import oci
from ociextirpater.OCIClient import OCIClient

class managementagent( OCIClient ):
    service_name = "Management Agent"
    clientClass = oci.management_agent.ManagementAgentClient

    objects = [
        {
            "function_list"    : "list_management_agent_install_keys",
            "function_delete"  : "delete_management_agent_install_key",
            "name_singular"    : "Management Install Key",
            "name_plural"      : "Management Install Keys",
        }
    ]
