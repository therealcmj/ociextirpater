import logging

import oci
from ociextirpater.OCIClient import OCIClient

class compute( OCIClient ):
    service_name = "Compute"
    clientClass = oci.core.ComputeClient
    compositeClientClass = oci.core.ComputeClientCompositeOperations

    # TODO: move predelete out of the class and into the object!

    objects = [
        {
            "name_singular"      : "Compute Instance",
            "name_plural"        : "Compute Instances",
            "function_list"      : "list_instances",
            "function_delete"    : "terminate_instance",
            "kwargs_delete"      : {
                                       "preserve_data_volumes_created_at_launch": False
                                   }
        },

        {
            "name_singular"      : "Compute Image",
            "name_plural"        : "Compute Images",
            "function_list"      : "list_images",
                                    # listing images returns all the images in the specified compartment PLUS those
                                    # provided by Oracle. You can easily tell the difference by checking whether
                                    # it has compartment_id = None or a string.
                                    # This lambda function causes delete to skip those provided by Oracle
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

        {
            "name_singular"      : "Dedicated VM Host",
            "name_plural"        : "Dedicated VM Hosts",

            "function_list"      : "list_dedicated_vm_hosts",
            "function_delete"    : "delete_dedicated_vm_host",
        },


        # Other services to consider
        # list_compute_global_image_capability_schemas
        # list_vnic_attachments
    ]
