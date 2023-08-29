import oci
from ociextirpater.OCIClient import OCIClient

class waf( OCIClient ):
    service_name = "Web App Firewall"
    clientClass = oci.waf.WafClient

    objects = [
        {
            "name_singular"      : "Web App Firewall",
            "name_plural"        : "Web App Firewalls",

            "function_list"      : "list_web_app_firewall_policies",
            # "formatter"          : lambda instance: "XXX instance with OCID {} / name '{}' is in state {}".format( instance.id, instance.name, instance.lifecycle_state ),
            "function_delete"    : "delete_web_app_firewall_policy",
        },
    ]


#list_network_address_lists
