import oci
from ociextirpater.OCIClient import OCIClient

import logging

class loganalytics( OCIClient ):
    service_name = "Log Analytics"
    clientClass = oci.log_analytics.LogAnalyticsClient

    namespace = None
    def __init__(self,config):
        super().__init__(config)

        # we need the namespace
        self.namespace = self.clients[ config.home_region ].list_namespaces(config.ociconfig["tenancy"]).data.items[0].namespace_name
        logging.debug("Logging Analytics namespace is {}".format(self.namespace))

    objects = [
        # # this is a very special one - storage
        # {
        #     "name_singular"      : "Storage",
        #     "name_plural"        : "Storage",
        #
        #     # # "formatter"          : lambda instance: "XXX instance with OCID {} / name '{}' is in state {}".format( instance.id, instance.name, instance.lifecycle_state ),
        #     # "function_list"      : "list_xxx",
        #     # "function_delete"    : "delete_xxx",
        # },

        {
            "formatter"          : lambda obj: "Log Analytics Entity with OCID {} / name '{}' is in state {}".format( obj.id, obj.name, obj.lifecycle_state ),

            "function_list"      : "list_log_analytics_entities",
            # "function_delete"    : "delete_log_analytics_entity",
            "name_singular"      : "Log Analytics Entity",
            "name_plural"        : "Log Analytics Entities",
        },

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

    # I override the findAllInCompartment from OCIClient.py because Log Analytics has an extra param
    def findAllInCompartment(self, region, o, this_compartment, **kwargs):
        logging.debug("Calling {}".format( o["function_list"]))
        os = oci.pagination.list_call_get_all_results(getattr((self.clients[region]), o["function_list"]),
                                                      self.namespace,
                                                      this_compartment,
                                                      **kwargs).data
        return os

    def delete_object(self, object, region, found_object):
        if object["name_singular"] == "Log Analytics Entity":
            return (self.clients[region]).delete_log_analytics_entity(
                self.namespace,
                found_object.id
            )

        elif object["name_singular"] == "Log Analytics Log Group":
            return (self.clients[region]).delete_log_analytics_log_group(
                self.namespace,
                found_object.id
            )

        raise NotImplementedError
