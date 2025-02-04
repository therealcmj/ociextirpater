import logging
import oci
from ociextirpater.OCIClient import OCIClient

class vb( OCIClient ):
    service_name = "Visual Builder"
    clientClass = oci.visual_builder.VbInstanceClient

    objects = [
        {
            "name_singular"      : "Visual Builder Instance",
            "name_plural"        : "Visual Builder Instances",
            "function_list"      : "list_vb_instances",
            "function_delete"    : "delete_vb_instance",
        },
    ]
