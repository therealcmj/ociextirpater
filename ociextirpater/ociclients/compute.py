import logging

import oci
from ociextirpater.OCIClient import OCIClient

class compute( OCIClient ):
    service_name = "Compute"
    clientClass = oci.core.ComputeClient
    compositeClientClass = oci.core.ComputeClientCompositeOperations

    # TODO: move predelete out of the class and into the object!
    def predelete(self,object,region,found_object):
        if object["name_singular"] == "Compute Instance":
            logging.debug("In my pre-delete function")
            if found_object.lifecycle_state == "RUNNING":
                logging.info("Stopping instance before terminating")
                # TODO: switch to composite client and wait for instance to stop
                # self.clients[region].instance_action( found_object.id, "STOP" )
                self.compositeClients[region].instance_action_and_wait_for_state(found_object.id, "STOP" , wait_for_states=["STOPPED"])
        return

    objects = [
        {
            "name_singular"      : "Compute Instance",
            "name_plural"        : "Compute Instances",
            "function_list"      : "list_instances",
            "function_delete"    : "terminate_instance",
        },

        {
            "name_singular"      : "Compute Image",
            "name_plural"        : "Compute Images",
            "function_list"      : "list_images",
            "check2delete"       : lambda image: hasattr( image,"compartment_id") and image.compartment_id != None,
            "function_delete"    : "delete_image",
        },

        {
            "name_singular"      : "Compute Capacity Reservation",
            "name_plural"        : "Compute Capacity Reservations",

            "function_list"      : "list_compute_capacity_reservations",
            "function_delete"    : "delete_compute_capacity_reservation",
        },

        {
            "name_singular"      : "Compute Cluster",
            "name_plural"        : "Compute Clusters",

            "function_list"      : "list_compute_clusters",
            "function_delete"    : "delete_compute_cluster",
        },

        # Other services to consider
        # list_compute_global_image_capability_schemas
        # list_dedicated_vm_hosts
        # list_vnic_attachments
    ]
