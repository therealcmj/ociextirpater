import oci
from ociextirpater.OCIClient import OCIClient

class waa( OCIClient ):
    service_name = "Web App Accelerator"
    clientClass = oci.waa.WaaClient

    objects = [
        {
            "name_singular"      : "Web App Acceleration Policy",
            "name_plural"        : "Web App Acceleration Policies",
            "function_list"      : "list_web_app_acceleration_policies",
            "function_delete"    : "delete_web_app_acceleration_policy",
        },
    ]
