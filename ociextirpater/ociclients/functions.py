import oci
from ociextirpater.OCIClient import OCIClient

class functions( OCIClient ):
    service_name = "Functions"
    clientClass = oci.functions.FunctionsManagementClient

    objects = [
        {
            "function_list"    : "list_applications",
            "function_delete"  : "delete_application",
            "name_singular"    : "Functions Application",
            "name_plural"      : "Functions Applications",
        }
    ]
