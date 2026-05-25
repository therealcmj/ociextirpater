import oci
from ociextirpater.OCIClient import OCIClient

class dataintegration( OCIClient ):
    service_name = "Data Integration"
    clientClass = oci.data_integration.DataIntegrationClient

    objects = [
        {
            "name_singular"      : "Data Integration Workspace",
            "name_plural"        : "Data Integration Workspaces",
            "function_list"      : "list_workspaces",
            "function_delete"    : "delete_workspace",
            "kwargs_delete"      :  {
                                        "is_force_operation": True,
                                        "quiesce_timeout": 1,
                                    }
        },
    ]
