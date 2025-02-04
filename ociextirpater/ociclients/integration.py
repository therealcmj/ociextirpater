import logging
import oci
from ociextirpater.OCIClient import OCIClient

class integration( OCIClient ):
    service_name = "Integration Cloud"
    clientClass = oci.integration.IntegrationInstanceClient

    objects = [
        {
            "name_singular"      : "Integration Instance",
            "name_plural"        : "Integration Instances",
            "function_list"      : "list_integration_instances",
            "function_delete"    : "delete_integration_instance",
        },
    ]
