import logging
import oci
from ociextirpater.OCIClient import OCIClient

class containerinstance( OCIClient ):
    service_name = "Container Instance"
    clientClass = oci.container_instances.ContainerInstanceClient

    objects = [
        {
            "name_singular"      : "Container Instance",
            "name_plural"        : "Container Instances",
            "function_list"      : "list_container_instances",
            "function_delete"    : "delete_container_instance",
        },

    ]
