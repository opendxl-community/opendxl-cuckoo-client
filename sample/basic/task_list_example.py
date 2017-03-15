# This sample invokes and displays the results of the "tasks/list" command via
# the Cuckoo DXL service. The results of the find command are displayed in JSON
# format.
#
#
#

import json
import os
import sys

from dxlclient.client_config import DxlClientConfig
from dxlclient.client import DxlClient
from dxlcuckooclient import CuckooClient

# Import common logging and configuration
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from common import *

# Configure local logger
logging.getLogger().setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

# Create DXL configuration from file
config = DxlClientConfig.create_dxl_config_from_file(CONFIG_FILE)

CUCKOO_COMMAND = "tasks/list"

# Create the client
with DxlClient(config) as client:


    
    # Connect to the fabric
    client.connect()

    # Create the Cuckoo client
    cuckoo_client = CuckooClient(client)

    # Run the CUCKOO command
    res = cuckoo_client.run_command(CUCKOO_COMMAND)

    print res
