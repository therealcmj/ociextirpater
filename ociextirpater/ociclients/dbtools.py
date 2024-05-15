import oci
from ociextirpater.OCIClient import OCIClient

class dbtools( OCIClient ):
    service_name = "Database Tools"
    clientClass = oci.database_tools.DatabaseToolsClient

    objects = [

        # list_database_tools_connections(…)
        {
            "function_list"      : "list_database_tools_connections",
            # "kwargs_list"        : {
            #                             # "lifecycle_state": ["ACTIVE","FAILED"]
            #                        },
            "function_delete"    : "delete_database_tools_connection",
            "name_singular"      : "Database Tools Connection",
            "name_plural"        : "Database Tools Connections",
        },

        # list_database_tools_private_endpoints(…)
        {
            "function_list"      : "list_database_tools_private_endpoints",
            "function_delete"    : "delete_database_tools_private_endpoint",
            "name_singular"      : "Database Tools Private Endpoint",
            "name_plural"        : "Database Tools Private Endpoints",
        },

        # {
        #     # "formatter"          : lambda instance: "XXX instance with OCID {} / name '{}' is in state {}".format( instance.id, instance.name, instance.lifecycle_state ),
        #     "function_list"      : "list_xxx",
        #     "kwargs_list"        : {
        #                            },
        #     "function_delete"    : "delete_xxx",
        #     "name_singular"      : "XXX",
        #     "name_plural"        : "XXXXs",
        # },

    ]
