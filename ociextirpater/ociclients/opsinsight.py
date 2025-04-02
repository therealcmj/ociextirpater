import logging
import oci
from ociextirpater.OCIClient import OCIClient

class opsinsight( OCIClient ):
    service_name = "Operations Insight"
    clientClass = oci.opsi.OperationsInsightsClient

    objects = [
        {
            "name_singular"      : "Private Endpoint",
            "name_plural"        : "Private Endpoints",
            # "function_list"      : "list_operations_insights_private_endpoints",
            "function_delete"    : "delete_operations_insights_private_endpoint",
        },

        {
            "name_singular"      : "Database Insight",
            "name_plural"        : "Database Insights",
            "formatter"          : lambda insight: "Database Insight with OCID {} for database name '{}' is in state {}".format(insight.id, insight.database_name, insight.lifecycle_state),
            "function_delete"    : "delete_database_insight",
        },

        {
            "name_singular"      : "Host Insight",
            "name_plural"        : "Host Insights",
            "formatter"          : lambda insight: "Host Insight with OCID {} for host name '{}' is in state {}".format(insight.id, insight.host_name, insight.lifecycle_state),
            # list_host_insights
            "function_delete"    : "delete_host_insight",
        },

        {
            "name_singular"      : "Enterprise Manager Bridge",
            "name_plural"        : "Enterprise Manager Bridges",
            # list_enterprise_manager_bridges
            "function_delete"    : "delete_enterprise_manager_bridge",
        },


        # haven't implemented these yet
        # delete_news_report
        # delete_awr_hub
        # delete_awr_hub_source
        # delete_operations_insights_warehouse
        # delete_operations_insights_warehouse_user
        # delete_opsi_configuration
    ]

    def findAllInCompartment(self, region, o, this_compartment, **kwargs):
        if o["name_plural"] == "Private Endpoints":
            return oci.pagination.list_call_get_all_results(
                getattr((self.clients[region]), "list_operations_insights_private_endpoints"),
                **{"compartment_id":this_compartment}).data

        if o["name_plural"] == "Database Insights":
            return oci.pagination.list_call_get_all_results(
                getattr(
                    (self.clients[region]), "list_database_insights"),
                    **{
                        "compartment_id":this_compartment,
                        "status": [ "DISABLED", "ENABLED", "TERMINATED" ]
                    }).data

        if o["name_plural"] == "Host Insights":
            return oci.pagination.list_call_get_all_results(
                getattr((self.clients[region]), "list_host_insights"),
                **{
                    "compartment_id": this_compartment,
                    "status": ["DISABLED", "ENABLED", "TERMINATED"],
                    "lifecycle_state": [ "CREATING", "UPDATING", "ACTIVE", "FAILED", "NEEDS_ATTENTION" ],
                }).data

        if o["name_plural"] == "Enterprise Manager Bridges":
            return oci.pagination.list_call_get_all_results(
                getattr((self.clients[region]), "list_enterprise_manager_bridges"),
                **{
                    "compartment_id": this_compartment,
                    # "status": ["DISABLED", "ENABLED", "TERMINATED"],
                    # "lifecycle_state": [ "CREATING", "UPDATING", "ACTIVE", "DELETING", "DELETED", "FAILED", "NEEDS_ATTENTION" ],
                }).data

        raise NotImplementedError

    def predelete(self,object,region,found_object):
        if found_object.status == "DISABLED":
            logging.info("Already disabled.")
            return

        if object["name_plural"] == "Database Insights":
            f = getattr((self.clients[region]), "disable_database_insight")
            logging.info("Disabling {}".format( object["name_singular"]))
            f(found_object.id)
            return

        if object["name_plural"] == "Host Insights":
            f = getattr((self.clients[region]), "disable_host_insight")
            logging.info("Disabling {}".format( object["name_singular"]))
            f(found_object.id)
            return

        raise NotImplementedError

