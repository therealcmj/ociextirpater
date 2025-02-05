import logging
import oci
from ociextirpater.OCIClient import OCIClient

class dataflow( OCIClient ):
    service_name = "Data Flow"
    clientClass = oci.data_flow.DataFlowClient

    objects = [
        # {
        #     "name_singular"      : "Run",
        #     "name_plural"        : "Runs",
        #     "function_list"      : "list_runs",
        #     "function_delete"    : "delete_run",
        # },

        {
            "name_singular"      : "Application",
            "name_plural"        : "Applications",
            "function_list"      : "list_applications",
            "function_delete"    : "delete_application",
        },

        {
            "name_singular"      : "Pool",
            "name_plural"        : "Pools",
            "function_list"      : "list_pools",
            "function_delete"    : "delete_pool",
        },

        {
            "name_singular"      : "Private Endpoint",
            "name_plural"        : "Private Endpoints",
            "function_list"      : "list_private_endpoints",
            "function_delete"    : "delete_private_endpoint",
        },

    ]
