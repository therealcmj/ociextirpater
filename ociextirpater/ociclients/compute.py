import logging

import oci
from ociextirpater.OCIClient import OCIClient

class compute( OCIClient ):
    service_name = "Compute"
    clientClass = oci.core.ComputeClient

    def predelete(self,object,region,found_object):
        logging.debug("In my pre-delete function")
        if object.lifecycle_state == "RUNNING":
            logging.info("Stopping instance before terminating")
            self.clients[region].instance_action( found_object.id, "STOP" )
        return

    objects = [
        {
            "function_list"      : "list_instances",
            "kwargs_list"        : {
                                   },
            "function_delete"    : "terminate_instance",
            "name_singular"      : "Compute Instance",
            "name_plural"        : "Compute Instances",
        },
    ]
