import oci
from ociextirpater.OCIClient import OCIClient


class stackmonitoring(OCIClient):
    service_name = "Stack Monitoring"
    clientClass = oci.stack_monitoring.StackMonitoringClient

    objects = [
        # TODO check these:
        # list_baselineable_metrics **
        # delete_baselineable_metric
        #
        # list_metric_extensions **
        # delete_metric_extension

        {
            "name_singular"      : "Discovery Job",
            "name_plural"        : "Discovery Jobs",
            "function_list"      : "list_discovery_jobs",
            "formatter"          : lambda job: "Discovery Job with OCID {} / name '{}' is in state {}".format(job.id, job.resource_name, job.lifecycle_state),

            "function_delete"    : "delete_discovery_job",
        },

        {
            "name_singular"      : "Monitored Resource",
            "name_plural"        : "Monitored Resources",
            "function_list"      : "list_monitored_resources",
            "function_delete"    : "delete_monitored_resource",
        },

        {
            "name_singular"      : "Maintenance Window",
            "name_plural"        : "Maintenance Windows",
            "function_list"      : "list_maintenance_windows",
            "function_delete"    : "delete_maintenance_window",
        },

        {
            "name_singular"      : "List Monitored Resource Type",
            "name_plural"        : "List Monitored Resource Types",
            "function_list"      : "list_monitored_resource_types",
            "kwargs_list"        : {
                                        "is_exclude_system_types": True
                                   },

            "function_delete"    : "delete_monitored_resource_type",
        },

        {
            "name_singular"      : "Process Set",
            "name_plural"        : "Process Sets",
            "function_list"      : "list_process_sets",
            "function_delete"    : "delete_process_set",
        },

        {
            "name_singular"      : "Config",
            "name_plural"        : "Configs",
            "function_list"      : "list_configs",
            "function_delete"    : "delete_config",
        },
    ]
