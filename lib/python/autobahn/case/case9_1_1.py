###############################################################################
##
##  Copyright 2011 Tavendo GmbH
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
###############################################################################

from case import Case

class Case9_1_1(Case):

   DESCRIPTION = """Send text message message with payload of length 2**20 (1M). Sent out data in chops of 997 octets."""

   EXPECTATION = """Receive echo'ed text message (with payload as sent)."""

   def init(self):
      self.DATALEN = 2**20
      self.PAYLOAD = "BAsd7&jh23..-"
      self.WAITSECS = 10

   def onOpen(self):
      self.p.createWirelog = False
      self.passed = False
      self.result = "Error - Did not receive message within %d seconds." % self.WAITSECS

      self.p.sendFrame(opcode = 1, payload = self.PAYLOAD, payload_len = self.DATALEN, chopsize = 997)
      self.p.killAfter(self.WAITSECS)

   def onMessage(self, msg, binary):
      if binary:
         self.passed = False
         self.result = "Error - Expected text message with payload, but got binary."
      else:
         if len(msg) != self.DATALEN:
            self.passed = False
            self.result = "Error - Expected text message with payload of length %d, but got %d." % (self.DATALEN, len(msg))
         else:
            ## FIXME : check actual content
            ##
            self.passed = True
            self.result = "Ok - Received text message of length %d." % len(msg)
      self.p.failConnection()

   def onConnectionLost(self, failedByMe):
      pass