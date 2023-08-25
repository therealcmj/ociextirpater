import oci
from ociextirpater.OCIClient import OCIClient

class npa( OCIClient ):
    service_name = "Network Path Analysis"
    clientClass = oci.vn_monitoring.VnMonitoringClient

    objects = [
        {
            "name_singular"      : "Network Path Analyzer Test",
            "name_plural"        : "Network Path Analyzer Tests",


            "function_list"      : "list_path_analyzer_tests",
        #     "formatter"          : lambda instance: "XXX instance with OCID {} / name '{}' is in state {}".format( instance.id, instance.name, instance.lifecycle_state ),
            "function_delete"    : "delete_path_analyzer_test",
        },
    ]
