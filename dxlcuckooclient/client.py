# -*- coding: utf-8 -*-
################################################################################
# Copyright (c) 2017 McAfee Inc. - All Rights Reserved.
################################################################################

import json
import logging
from dxlclient import Request, Message

# Configure local logger
logger = logging.getLogger(__name__)



class CuckooClient(object):
    """
    This client provides a high level wrapper for invoking cuckoo remote commands via the
    Data Exchange Layer (DXL) fabric.

    The purpose of this library is to allow users to invoke cuckoo remote commands without having to focus
    on lower-level details such as cuckoo-specific DXL topics and message formats.
    """

    # The type of the Cuckoo DXL service that is registered with the fabric
    DXL_SERVICE_TYPE = "/mcafee/service/cuckoo/remote"

    # The default amount of time (in seconds) to wait for a response from the Cuckoo DXL service
    DEFAULT_RESPONSE_TIMEOUT = 30

    # The minimum amount of time (in seconds) to wait for a response from the Cuckoo DXL service
    MIN_RESPONSE_TIMEOUT = 300

    # Encoding used to encode/decode DXL payloads
    _UTF_8 = "utf-8"

    def __init__(self, dxl_client):
        """

        Constructor parameters:

        :param dxl_client: The DXL client to use for communication with the Cuckoo DXL service
        """
        self._dxl_client = dxl_client
        self._response_timeout = self.DEFAULT_RESPONSE_TIMEOUT

    @property
    def response_timeout(self):
        """
        The maximum amount of time (in seconds) to wait for a response from the Cuckoo service
        """
        return self._response_timeout

    @response_timeout.setter
    def response_timeout(self, response_timeout):
        if response_timeout < self.MIN_RESPONSE_TIMEOUT:
            raise Exception("Response timeout must be greater than or equal to " + str(self.MIN_RESPONSE_TIMEOUT))
        self._response_timeout = response_timeout

    def run_command(self, command_name):
        """
        Invokes a Cuckoo remote command on the Cuckoo server this client is communicating with.

        **Example Usage**

            .. code-block:: python

                # Run the system find command
                result = cuckoo_client.run_command("/tasks/list",
                                                output_format=OutputFormat.JSON)

        **Example Response**

            .. code-block:: python

                [
                    {
                        ...

                    }
                ]

        :param command_name: The name of the remote command to invoke
        :param params: (optional) A dictionary (``dict``) containing the parameters for the command
        :param output_format: (optional) The output format for Cuckoo to use when returning the response.
            The list of `output formats` can be found in the :class:`OutputFormat` constants class.
        :return: The result of the remote command execution
        """

        return self._invoke_cuckoo_service({
            "command": command_name
        })

    def _invoke_cuckoo_service(self, payload_dict):
        """
        Invokes the Cuckoo DXL service for the purposes of executing a remote command
        :param payload_dict: The dictionary (``dict``) to use as the payload of the DXL request
        :return: The result of the remote command execution
        """
	print "payload_dict"
	print payload_dict
	print "\n"
        return self._sync_request(
            self._dxl_client,
            Request(self.DXL_SERVICE_TYPE),
            self._response_timeout,
            payload_dict)

    @staticmethod
    def _sync_request(dxl_client, request, response_timeout, payload_dict):
        """
        Performs a synchronous DXL request and returns the payload

        :param dxl_client: The DXL client with which to perform the request
        :param request: The DXL request to send
        :param response_timeout: The maximum amount of time to wait for a response
        :param payload_dict: The dictionary (``dict``) to use as the payload of the DXL request
        :return: The result of the remote command execution (resulting payload)
        """
        # Set the payload
        request.payload = json.dumps(payload_dict).encode(encoding=CuckooClient._UTF_8)

        # Display the request that is going to be sent
        logger.debug("Request:\n{0}".format(
            json.dumps(payload_dict, sort_keys=True, indent=4, separators=(',', ': '))))

        # Send the request and wait for a response (synchronous)
        res = dxl_client.sync_request(request, timeout=response_timeout)

        # Return a dictionary corresponding to the response payload
        if res.message_type != Message.MESSAGE_TYPE_ERROR:
            ret_val = res.payload.decode(encoding=CuckooClient._UTF_8)
            # Display the response
            logger.debug("Response:\n{0}".format(ret_val))
            return ret_val
        else:
            raise Exception("Error: " + res.error_message + " (" + str(res.error_code) + ")")

