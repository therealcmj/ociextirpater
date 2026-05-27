import oci
from ociextirpater.OCIClient import OCIClient

class waas( OCIClient ):
    service_name = "Web Application Acceleration and Security",
    clientClass = oci.waas.WaasClient
    isRegional = False

    objects = [
        {
            "name_singular"      : "WAAS Policy",
            "name_plural"        : "WAAS Policies",
            "function_list"      : "list_waas_policies",
            "function_delete"    : "delete_waas_policy",
        },

        {
            "name_singular"      : "WAAS Custom Protection Rule",
            "name_plural"        : "WAAS Custom Protection Rules",
            "function_list"      : "list_custom_protection_rules",
            "function_delete"    : "delete_custom_protection_rule",
        },

        {
            "name_singular"      : "WAAS Address List",
            "name_plural"        : "WAAS Address Lists",
            "function_list"      : "list_address_lists",
            "function_delete"    : "delete_address_list",
        },

        {
            "name_singular"      : "WAAS Certificate",
            "name_plural"        : "WAAS Certificates",
            "function_list"      : "list_certificates",
            "function_delete"    : "delete_certificate",
        },
    ]
