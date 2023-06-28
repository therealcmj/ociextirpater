import logging

import oci
from ociextirpater.OCIClient import OCIClient

class computepool( OCIClient ):
    service_name = "Compute Instance Pool"
    clientClass = oci.core.ComputeManagementClient

    # TODO?
    # def predelete(self,object,region,found_object):
    #     logging.debug("In my pre-delete function")
    #     if object.lifecycle_state == "RUNNING":
    #         logging.info("Stopping instance before terminating")
    #         self.clients[region].instance_action( found_object.id, "STOP" )
    #     return

    objects = [
        {
            "function_list"      : "list_instance_pools",
            "kwargs_list"        : {
                                   },
            "function_delete"    : "terminate_instance_pool",
            "name_singular"      : "Compute Instance Pool",
            "name_plural"        : "Compute Instance Pools",
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
