import oci
from ociextirpater.OCIClient import OCIClient

class healthchecks( OCIClient ):
    service_name = "Health Checks"
    clientClass = oci.healthchecks.HealthChecksClient

    objects = [
        {
            "name_singular"      : "HTTP Monitor",
            "name_plural"        : "HTTP Monitors",

            "function_list"      : "list_http_monitors",
            "formatter"          : lambda check: "HTTP Monitor with OCID {} / name '{}'".format(check.id, check.display_name),
            "function_delete"    : "delete_http_monitor",
        },

        {
            "name_singular"      : "Ping Monitor",
            "name_plural"        : "Ping Monitors",

            "function_list"      : "list_ping_monitors",
            "formatter"          : lambda check: "Ping Monitor with OCID {} / name '{}'".format(check.id, check.display_name),
            "function_delete"    : "delete_ping_monitor",
        },
    ]
