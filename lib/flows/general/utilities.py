#!/usr/bin/env python
# Copyright 2011 Google Inc. All Rights Reserved.

"""Flows that often get reused by other flows."""



import logging
import stat

from grr.lib import aff4
from grr.lib import flow
from grr.lib import rdfvalue
from grr.proto import flows_pb2


class DownloadDirectoryArgs(rdfvalue.RDFProtoStruct):
  protobuf = flows_pb2.DownloadDirectoryArgs


class DownloadDirectory(flow.GRRFlow):
  """Flow for recursively downloading all files in a directory."""

  category = "/Filesystem/"

  args_type = DownloadDirectoryArgs

  @flow.StateHandler(next_state="DownloadDir")
  def Start(self, unused_response):
    """Issue a request to list the directory."""
    self.state.Register("out_urn", None)
    self.CallClient("ListDirectory", pathspec=self.state.args.pathspec,
                    next_state="DownloadDir",
                    request_data=dict(depth=self.state.args.depth))

  @flow.StateHandler(next_state=["DownloadDir", "Done"])
  def DownloadDir(self, responses):
    """Download all files in a given directory recursively."""

    if not responses.success:
      if not self.state.args.ignore_errors:
        err = "Error downloading directory: %s" % responses.status
        logging.error(err)
        raise flow.FlowError(err)
    else:
      depth = responses.request_data["depth"] - 1

      for stat_response in responses:
        # Retrieve where the files are being stored in the VFS.
        if not self.state.out_urn:
          self.state.out_urn = aff4.AFF4Object.VFSGRRClient.PathspecToURN(
              stat_response.pathspec, self.client_id).Dirname()

        if stat.S_ISDIR(stat_response.st_mode):
          # No need to traverse subdirectories if the current depth is 0
          if depth > 0:
            self.CallClient("ListDirectory", next_state="DownloadDir",
                            pathspec=stat_response.pathspec,
                            request_data=dict(depth=depth))
        else:
          if stat.S_ISREG(stat_response.st_mode):
            self.CallFlow("GetFile", pathspec=stat_response.pathspec,
                          next_state="Done")

  @flow.StateHandler()
  def Done(self, responses):
    if not responses.success:
      if not self.state.args.ignore_errors:
        err = "Error downloading file %s" % responses.status
        logging.error(err)
        raise flow.FlowError(err)

  @flow.StateHandler()
  def End(self):
    if self.state.out_urn:
      self.Notify("ViewObject", self.state.out_urn,
                  "Completed DownloadDirectory")
