#!/usr/bin/env python
"""Filestore aff4:/files abstraction layer.

Filestore allows for multiple different filestore modules to register URNs
under aff4:/files to handle new file hash and new file creations.
"""

from grr.parsers import fingerprint
from grr.lib import access_control
from grr.lib import aff4
from grr.lib import data_store
from grr.lib import rdfvalue
from grr.lib import registry


class FileStoreInit(registry.InitHook):
  """Create filestore aff4 paths."""

  pre = ["GRRAFF4Init"]

  def Run(self):
    """Create FileStore and HashFileStore namespaces."""
    try:
      filestore = aff4.FACTORY.Create(FileStore.PATH, "FileStore",
                                      mode="rw", token=aff4.FACTORY.root_token)
      filestore.Close()

      hash_urn = rdfvalue.RDFURN(FileStore.PATH).Add(HashFileStore.PATH)
      hash_filestore = aff4.FACTORY.Create(hash_urn, "HashFileStore",
                                           mode="rw",
                                           token=aff4.FACTORY.root_token)
      hash_filestore.Close()
    except access_control.UnauthorizedAccess:
      # The aff4:/files area is ACL protected, this might not work on components
      # that have ACL enforcement.
      pass


class FileStore(aff4.AFF4Volume):
  """Filestore for files downloaded from clients.

  Modules can register for file content by creating paths under "aff4:/files".
  By default files created in this namespace can be read by users that have the
  URN (hash).  See lib/aff4_objects/user_managers.py.
  """
  PATH = "aff4:/files"
  CHUNK_SIZE = 5 * 512 * 1024

  def CheckHashes(self, hashes, hash_type="sha256"):
    """Checks a list of hashes for presence in the store.

    Args:
      hashes: A list of Hash objects to check.
      hash_type: The type of hash (can be sha256, sha1, md5).

    Yields:
      Tuples of  (urn, hash) of objects that exist in the store.
    """
    hashes = set(hashes)
    for child in self.OpenChildren():
      for urn, digest in child.CheckHashes(hashes, hash_type=hash_type):
        yield urn, digest

        hashes.discard(digest)

      # Nothing to search for, we are done.
      if not hashes:
        break

  def AddFile(self, blob_fd, sync=False):
    """Create a new file in the file store.

    We delegate the actual file addition to our contained
    implementations. Implementations can either implement the AddFile() method,
    returning a file like object which will be written on, or directly support
    the AddBlobToStore() method which can copy the BlobImage efficiently.

    Args:
      blob_fd: BlobImage open for read/write.
      sync: Should the file be synced immediately.
    """
    files_for_write = []
    for sub_store in self.OpenChildren():
      new_file = sub_store.AddFile(blob_fd, sync=sync)
      if new_file:
        files_for_write.append(new_file)

    blob_fd.Seek(0)
    while files_for_write:
      # If we got filehandles back, send them the data.
      data = blob_fd.Read(self.CHUNK_SIZE)
      if not data: break

      for child in files_for_write:
        child.Write(data)

    for child in files_for_write:
      child.Close(sync=sync)


class HashFileStore(FileStore):
  """FileStore that stores files referenced by hash."""

  PATH = "hash"

  def CheckHashes(self, hashes, hash_type="sha256"):
    """Check hashes against the filestore.

    Blobs use the hash in the schema:
    aff4:/files/hash/generic/sha256/[sha256hash]

    Args:
      hashes: A list of HashDigest objects to check.
      hash_type: The type of hash (can be sha256, sha1, md5).

    Yields:
      Tuples of (urn, hash) of objects that exist in the store.
    """
    hash_map = {}
    for digest in hashes:
      # The canonical name of the file is where we store the file hash.
      hash_map[aff4.ROOT_URN.Add("files/hash/generic").Add(hash_type).Add(
          str(digest))] = digest

    for metadata in aff4.FACTORY.Stat(list(hash_map), token=self.token):
      yield metadata["urn"], hash_map[metadata["urn"]]

  def AddFile(self, blob_fd, sync=False):
    """Accept a blobimage, hash the content, and create FileStoreImage objects.

    We take a blobimage in the client space:
      aff4:/C.123123123/fs/os/usr/local/blah

    Hash it, update the hash in the original blob image if its different to the
    one calculated on the client, and create FileStoreImages at the following
    URNs (if they don't already exist):

      aff4:/files/hash/generic/sha256/123123123 (canonical reference)
      aff4:/files/hash/generic/sha1/345345345
      aff4:/files/hash/generic/md5/456456456
      aff4:/files/hash/pecoff/md5/aaaaaaaa (only for PEs)
      aff4:/files/hash/pecoff/sha1/bbbbbbbb (only for PEs)

    When present in PE files, the signing data (revision, cert_type,
    certificate) is added to the original client-space blobimage.

    This can't be done simply in the FileStore.Write() method with fixed hash
    buffer sizes because the authenticode hashes need to track hashing of
    different-sized regions based on the signature information.

    Args:
      blob_fd: BlobImage open for reading.
      sync: Should the file be synced immediately.

    Raises:
      IOError: If there was an error writing the file.
    """
    if not isinstance(blob_fd, aff4.BlobImage):
      raise IOError("Only adding BlobImage to file store supported right now.")

    # Currently we only handle blob images.
    fingerprinter = fingerprint.Fingerprinter(blob_fd)
    fingerprinter.EvalGeneric()
    fingerprinter.EvalPecoff()

    hashes = blob_fd.Schema.HASH()
    signed_data = None
    file_store_files = []

    for result in fingerprinter.HashIt():
      fingerprint_type = result["name"]
      for hash_type in ["md5", "sha1", "sha256", "SignedData"]:
        if hash_type not in result:
          continue

        if hash_type == "SignedData":
          # There can be several certs in the same file.
          for signed_data in result[hash_type]:
            hashes.signed_data.Append(revision=signed_data[0],
                                      cert_type=signed_data[1],
                                      certificate=signed_data[2])
          continue

        # Set the hashes in the original object
        if fingerprint_type == "generic":
          hashes.Set(hash_type, result[hash_type])

        elif fingerprint_type == "pecoff":
          hashes.Set("pecoff_%s" % hash_type, result[hash_type])

        # These files are all created through async write so they should be
        # fast.
        hash_digest = result[hash_type].encode("hex")
        file_store_urn = aff4.ROOT_URN.Add("files/hash").Add(
            fingerprint_type).Add(hash_type).Add(hash_digest)

        file_store_fd = aff4.FACTORY.Create(file_store_urn, "FileStoreImage",
                                            mode="w", token=self.token)
        file_store_fd.FromBlobImage(blob_fd)
        file_store_fd.AddIndex(blob_fd.urn)

        file_store_files.append(file_store_fd)

    # Write the hashes attribute to all the created files..
    for fd in file_store_files:
      fd.Set(hashes)
      fd.Close(sync=sync)

    blob_fd.Set(hashes)

    # We do not want to be externally written here.
    return None


class FileStoreImage(aff4.BlobImage):
  """The AFF4 files that are stored in the file store area.

  Files in the file store are essentially blob images, containing indexes to the
  client files which matches their hash.

  It is possible to query for all clients which match a specific hash or a
  regular expression of the aff4 path to the files on these clients.

  e.g. on the console, you can query for all clients with a hash like this:

  In [31]: fd = aff4.FACTORY.Open("aff4:/files/hash/generic/sha256/2663a09072b9e
  a027ff1e3e3d21d351152c2534c2fe960a765c5321bfb7b6b25")

  In [32]: list(fd.Query("aff4:/C.+"))
  Out[32]: [<aff4:/C.f2614de8d636797e/fs/os/usr/share/gimp/2.0/images/wilber.png
  age=1970-01-01 00:00:00>]
  """

  class SchemaCls(aff4.BlobImage.SchemaCls):
    # The file store does not need to version file content.
    HASHES = aff4.Attribute("aff4:hashes", rdfvalue.HashList,
                            "List of hashes of each chunk in this file.",
                            versioned=False)

  def AddIndex(self, target):
    """Adds an indexed reference to the target URN."""
    predicate = ("index:target:%s" % target).lower()
    data_store.DB.MultiSet(self.urn, {predicate: target}, token=self.token,
                           replace=True, sync=False)

  def Query(self, target_regex, limit=100):
    """Search the index for matches to the file specified by the regex.

    Args:
       target_regex: The regular expression to match against the index.

       limit: Either a tuple of (start, limit) or a maximum number of results to
         return.

    Yields:
      URNs of files which have the same data as this file - as read from the
      index.
    """
    # Make the regular expression.
    regex = ["index:target:.*%s.*" % target_regex.lower()]
    start = 0
    try:
      start, length = limit
    except TypeError:
      length = limit

    # Get all the unique hits
    for i, (_, hit, _) in enumerate(data_store.DB.ResolveRegex(
        self.urn, regex, token=self.token, limit=limit)):

      if i < start: continue

      if i >= start + length:
        break

      yield rdfvalue.RDFURN(hit)
