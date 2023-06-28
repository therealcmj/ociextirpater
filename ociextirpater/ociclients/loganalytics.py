import oci
from ociextirpater.OCIClient import OCIClient

class loganalytics( OCIClient ):
    service_name = "Log Analytics"
    clientClass = oci.log_analytics.LogAnalyticsClient

    objects = [
        # {
        #     "function_list"      : "list_log_analytics_entities",
        #     "function_delete"    : "delete_log_analytics_entities",
        #     "name_singular"      : "Log Analytics Entity",
        #     "name_plural"        : "Log Analytics Entities",
        # },

        # {
        #     "function_list"      : "list_namespaces",
        #     "function_delete"    : "delete_namespace",
        #     "name_singular"      : "Namespace",
        #     "name_plural"        : "Namespaces",
        # },

        {
            "function_list"      : "list_log_analytics_log_groups",
            "function_delete"    : "delete_log_analytics_log_group",
            "name_singular"      : "Log Analytics Log Group",
            "name_plural"        : "Log Analytics Log Groups",
        },

        # {
        #     # "formatter"          : lambda instance: "XXX instance with OCID {} / name '{}' is in state {}".format( instance.id, instance.name, instance.lifecycle_state ),
        #     "function_list"      : "list_xxx",
        #     "function_delete"    : "delete_xxx",
        #     "name_singular"      : "XXX",
        #     "name_plural"        : "XXXXs",
        # },
    ]


    # def findAllInCompartment(self, region, o, this_compartment, **kwargs):
    #     # self.clients[region].list_log_analytics_log_groups()
    #     pass