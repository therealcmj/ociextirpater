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

        {
            "name_singular"      : "VSS Host Port Scan result",
            "name_plural"        : "VSS Host Port Scan results",

            "function_list"      : "list_host_port_scan_results",
            "function_delete"    : "delete_host_port_scan_result",
        },

        {
            "name_singular"      : "VSS Host Agent Scan result",
            "name_plural"        : "VSS Host Agent Scan results",

            "function_list"      : "list_host_agent_scan_results",
            "function_delete"    : "delete_host_agent_scan_result",
        },

        {
            "name_singular"      : "VSS CIS Benchmark Scan result",
            "name_plural"        : "VSS CIS Benchmark Scan results",

            "function_list"      : "list_host_cis_benchmark_scan_results",
            "function_delete"    : "delete_host_cis_benchmark_scan_result",
        },

        {
            "name_singular"      : "VSS Container Scan result",
            "name_plural"        : "VSS Container Scan results",

            "function_list"      : "list_container_scan_results",
            "formatter"          : lambda csr: "Container Scan result with OCID {} ".format(csr.id),
            "function_delete"    : "delete_container_scan_result",
        },

        {
            "name_singular"      : "VSS Container Scan Scan recipe",
            "name_plural"        : "VSS Container Scan Scan recipes",

            "function_list"      : "list_container_scan_recipes",
            "function_delete"    : "delete_container_scan_recipe",
        },

        {
            "name_singular"      : "VSS Container Scan target",
            "name_plural"        : "VSS Container Scan targets",

            "function_list"      : "list_container_scan_targets",
            "function_delete"    : "delete_container_scan_target",
        },


        # {
        #     "name_singular"      : "VSS Endpoint Protection Scan result",
        #     "name_plural"        : "VSS Endpoint Protection Scan results",
        #
        #     "function_list"      : "list_host_endpoint_protection_scan_results",
        #     "function_delete"    : "delete_host_endpoint_protection_scan_result",
        # },

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
