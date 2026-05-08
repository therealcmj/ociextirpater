import oci
from ociextirpater.OCIClient import OCIClient

class waf( OCIClient ):
    service_name = "Web App Firewall"
    clientClass = oci.waf.WafClient
    compositeClientClass = oci.waf.WafClientCompositeOperations

    _kwargs_delete_wait = {
                        "wait_for_states": [
                            oci.waf.models.WorkRequest.STATUS_SUCCEEDED,
                            oci.waf.models.WorkRequest.STATUS_FAILED,
                            ]
                    }

    objects = [
        {
            "name_singular"      : "Web App Firewall",
            "name_plural"        : "Web App Firewalls",
            "function_list"      : "list_web_app_firewalls",
            # in order to delete the policies you need to wait for all firewalls to be deleted. The next two lines allows for that.
            "c_function_delete"  : "delete_web_app_firewall_and_wait_for_state",
            "kwargs_delete"      :  _kwargs_delete_wait,
        },

        {
            "name_singular"      : "Web App Firewall Policy",
            "name_plural"        : "Web App Firewall Policies",
            "function_list"      : "list_web_app_firewall_policies",
            "function_delete"    : "delete_web_app_firewall_policy",
        },

        {
            "name_singular"      : "Web App Firewall Network address list",
            "name_plural"        : "Web App Firewall Network address lists",
            "function_list"      : "list_network_address_lists",
            "function_delete"    : "delete_network_address_list",
        },

    ]
