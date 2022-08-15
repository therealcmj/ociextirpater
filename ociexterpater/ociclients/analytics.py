import oci
from ociexterpater.OCIClient import OCIClient

class analytics( OCIClient ):
    service_name = "Analytics"
    clientClass = oci.analytics.AnalyticsClient

    objects = [
        {
            "formatter"          : lambda instance: "Analytics instance with OCID {} / name '{}' is in state {}".format( instance.id, instance.name, instance.lifecycle_state ),
            "function_list"      : "list_analytics_instances",
            "kwargs_list"        : {
                                   },
            # this isn't enough - we need to stop it AND wait for it to be stopped before we can delete it
            "function_predelete" : "stop_analytics_instance",
            "function_delete"    : "delete_analytics_instance",
            "name_singular"      : "Analytics instance",
            "name_plural"        : "Analytics instances",
        },
    ]
