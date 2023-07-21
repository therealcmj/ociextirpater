import oci
from ociextirpater.OCIClient import OCIClient

class vss( OCIClient ):
    service_name = "Vulnerability Scanning"
    clientClass = oci.vulnerability_scanning.VulnerabilityScanningClient
    compositeClientClass = oci.vulnerability_scanning.VulnerabilityScanningClientCompositeOperations

    objects = [
        {
            "name_singular"      : "VSS host scan target",
            "name_plural"        : "VSS host scan targets",

            "function_list"      : "list_host_scan_targets",
            "function_delete"    : "delete_host_scan_target",
        },


        {
            "name_singular"      : "VSS Host Scan recipe",
            "name_plural"        : "VSS Host Scan recipes",

            "function_list"      : "list_host_scan_recipes",
            "function_delete"    : "delete_host_scan_recipe",
        },

        # list_container_scan_recipes
        # list_container_scan_results
        # list_container_scan_targets
        # list_host_agent_scan_results
        # list_host_cis_benchmark_scan_results
        # list_host_endpoint_protection_scan_results


        # {
        #     "name_singular"      : "XXX",
        #     "name_plural"        : "XXXXs",

        #     "function_list"      : "list_xxx",
        #     "kwargs_list"        : {
        #                            },
        #     "formatter"          : lambda instance: "XXX instance with OCID {} / name '{}' is in state {}".format( instance.id, instance.name, instance.lifecycle_state ),
        #     "function_delete"    : "delete_xxx",
        # },
    ]
