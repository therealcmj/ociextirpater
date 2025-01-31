import oci
from ociextirpater.OCIClient import OCIClient

import logging

class loganalytics( OCIClient ):
    service_name = "Log Analytics"
    clientClass = oci.log_analytics.LogAnalyticsClient
    compositeClientClass = oci.log_analytics.LogAnalyticsClientCompositeOperations

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
            "name_singular"      : "Log Analytics Log Group",
            "name_plural"        : "Log Analytics Log Groups",
            "function_list"      : "list_log_analytics_log_groups",
            "formatter"          : lambda lg: "Log Group with OCID {} / name '{}'".format(lg.id, lg.display_name),
            # "function_delete"    : "delete_log_analytics_log_group",
        },

        {
            "name_singular"      : "Log Analytics Source",
            "name_plural"        : "Log Analytics Sources",
            "formatter"          : lambda source: "Logging source with name '{}' (ID {}) system defined: {}".format(source.name, source.source_id, source.is_system),
            "check2delete"       : lambda source: not source.is_system,
            "function_list"      : "list_sources",
            "kwargs_list"        : {
                                        "is_system": "CUSTOM"
                                   },

            # "function_delete"    : "delete_xxx",
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

        # special case. sources doesn't include the compartment id. So add it to each result
        if o["name_singular"] == "Log Analytics Source":
            for i in range(0,len(os)):
                logging.info("adding compartment")
                os[i].compartment_id = this_compartment

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

        elif object["name_singular"] == "Log Analytics Source":
            r = self.clients[region].get_source( self.namespace, found_object.name, found_object.compartment_id)
            return (self.clients[region]).delete_source(
                self.namespace,
                found_object.name,
                **{
                    "if_match": r.headers["ETag"]
                }
            )

        raise NotImplementedError
