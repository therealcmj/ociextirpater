import oci
from ociextirpater.OCIClient import OCIClient

class blockchain( OCIClient ):
    service_name = "Blockchain Platform"
    clientClass = oci.blockchain.BlockchainPlatformClient

    objects = [
        {
            "name_singular"      : "Blockchain Platform",
            "name_plural"        : "Blockchain Platforms",
            "function_list"      : "list_blockchain_platforms",
            "function_delete"    : "delete_blockchain_platform",
        },

    ]
