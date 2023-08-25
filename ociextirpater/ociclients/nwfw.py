import oci
from ociextirpater.OCIClient import OCIClient

class nwfw( OCIClient ):
    service_name = "Network Firewall"
    clientClass = oci.network_firewall.NetworkFirewallClient

    objects = [
        {
            "name_singular"      : "Network Firewall",
            "name_plural"        : "Network Firewalls",

            "function_list"      : "list_network_firewalls",
            "function_delete"    : "delete_network_firewall",
        },

        {
            "name_singular": "Network Firewall Policy",
            "name_plural": "Network Firewall Policies",

            "function_list": "list_network_firewall_policies",
            "function_delete": "delete_network_firewall_policy",
        },

    ]
