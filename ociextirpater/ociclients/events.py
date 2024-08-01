import oci
from ociextirpater.OCIClient import OCIClient

class events( OCIClient ):
    service_name = "Events"
    clientClass = oci.events.EventsClient

    objects = [
        {
            "name_singular"      : "Rule",
            "name_plural"        : "Rules",

            "function_list"      : "list_rules",
            "function_delete"    : "delete_rule",
        },
    ]
