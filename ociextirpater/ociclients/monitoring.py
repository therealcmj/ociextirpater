import oci
from ociextirpater.OCIClient import OCIClient

class monitoring( OCIClient ):
    service_name = "Monitoring"
    clientClass = oci.monitoring.MonitoringClient

    objects = [
        {
            "name_singular"      : "Alarm",
            "name_plural"        : "Alarms",

            "function_list"      : "list_alarms",
            "function_delete"    : "delete_alarm",
        },
    ]
