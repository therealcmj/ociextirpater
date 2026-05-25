import logging
import oci
from ociextirpater.OCIClient import OCIClient

class ocb( OCIClient ):
    service_name = "Cloud Bridge"
    clientClass = oci.cloud_bridge.ocb_agent_svc_client.OcbAgentSvcClient

    objects = [
        {
            "name_singular"      : "Environment",
            "name_plural"        : "Environments",
            "function_list"      : "list_environments",
            "function_delete"    : "delete_environment",
        },

        {
            "name_singular"      : "Agent",
            "name_plural"        : "Agents",
            "function_list"      : "list_agents",
            "function_delete"    : "delete_agent",
        },
    ]
