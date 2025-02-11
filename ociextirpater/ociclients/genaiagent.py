import logging
import oci
from ociextirpater.OCIClient import OCIClient

class genaiagent( OCIClient ):
    service_name = "GenAI Agent"
    clientClass = oci.generative_ai_agent.GenerativeAiAgentClient

    objects = [
        {
            "name_singular"      : "Agent Endpoint",
            "name_plural"        : "Agent Endpoints",
            "function_list"      : "list_agent_endpoints",
            "function_delete"    : "delete_agent_endpoint",
        },

        {
            "name_singular"      : "Agent",
            "name_plural"        : "Agents",
            "function_list"      : "list_agents",
            "function_delete"    : "delete_agent",
        },

        {
            "name_singular"      : "Data Ingestion Job",
            "name_plural"        : "Data Ingestion Jobs",
            "function_list"      : "list_data_ingestion_jobs",
            "function_delete"    : "delete_data_ingestion_job",
        },

        {
            "name_singular"      : "Data Source",
            "name_plural"        : "Data Sources",
            "function_list"      : "list_data_sources",
            "function_delete"    : "delete_data_source",
        },


        {
            "name_singular"      : "Knowledge Base",
            "name_plural"        : "Knowledge Bases",
            "function_list"      : "list_knowledge_bases",
            "function_delete"    : "delete_knowledge_base",
        },

    ]

    def findAllInCompartment(self, region, o, this_compartment, **kwargs):
        return oci.pagination.list_call_get_all_results(
            getattr((self.clients[region]), o["function_list"]),
            **{"compartment_id":this_compartment}).data

        # raise NotImplementedError
