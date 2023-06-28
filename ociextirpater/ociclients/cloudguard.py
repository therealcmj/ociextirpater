import oci
from ociextirpater.OCIClient import OCIClient

class cloudguard( OCIClient ):
    service_name = "Cloud Guard"
    clientClass = oci.cloud_guard.CloudGuardClient

    objects = [
        {
            "function_list"      : "list_security_zones",
            "function_delete"    : "delete_security_zone",
            "name_singular"      : "Security Zone",
            "name_plural"        : "Security Zones",
        },

        {
            "function_list"      : "list_targets",
            "function_delete"    : "delete_target",
            "name_singular"      : "Cloud Guard Target",
            "name_plural"        : "Cloud Guard Targets",
        },
    ]


