import logging
import oci
from ociextirpater.OCIClient import OCIClient

class genaiagent( OCIClient ):
    service_name = "GenAI Agent"
    clientClass = oci.generative_ai_agent.GenerativeAiAgentClient
    # compositeClientClass = oci.generative_ai_agent.GenerativeAiAgentClientCompositeOperations

    def __init__(self,config):
        super().__init__(config)
        # gen AI agents are only in limited regions
        # see https://docs.oracle.com/en-us/iaas/api/#/en/generative-ai-agents/20240531/ for the list
        # TODO 1: move this logic up into OCIClient
        # TODO 2: figure out how to detect if the service is available in the region and put THAT in the logic instead!
        # TODO 3: oy vey. This list is only OC1. That's going to be a problem for people cleaning up other realms
        for k in sorted(list(self.clients.keys())):
            if not k in [
                "ap-osaka-1",
                "eu-frankfurt-1",
                "sa-saopaulo-1",
                "uk-london-1",
                "us-ashburn-1",
                "us-chicago-1",
            ]:
                logging.info("Gen AI Agent service is NOT available in region {}. That region will be skipped".format(k))
                self.clients.pop(k)

            else:
                logging.info("Gen AI Agent service IS available in region {}".format(k))

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
            # "function_delete"    : "delete_agent",
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

    def predelete(self,object,region,found_object):
        # TODO: in Knowledge Bases check to make sure all of the data ingestion jobs are cleaned up
        return

    def delete_object(self, object, region, found_object):
        if object["name_plural"] == "Agents":
            logging.info("Listing tools associated with agent {}".format(found_object.id))
            f_list_tools = getattr((self.clients[region]), "list_tools")
            f_delete_tool = getattr((self.clients[region]), "delete_tool")
            f_delete_agent = getattr((self.clients[region]), "delete_agent")
            tools = oci.pagination.list_call_get_all_results(
                f_list_tools,
                **{"compartment_id": found_object.compartment_id},
                **{
                    "agent_id":found_object.id,
                    "lifecycle_state": "ACTIVE"
                    }
                ).data

            for tool in tools:
                logging.info( "Deleting tool {} associated with agent {}".format(tool.id, found_object.id) )
                f_delete_tool( tool.id )

            logging.debug("All tools associated with agent {} have been deleted. Now deleting the agent itself".format(found_object.id) )
            f_delete_agent(found_object.id)
            return
    
        raise NotImplementedError
