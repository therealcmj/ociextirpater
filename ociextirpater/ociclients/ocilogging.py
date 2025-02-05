import logging
import oci
from ociextirpater.OCIClient import OCIClient


# funny story - don't rename this "logging" for reasons!
class ocilogging( OCIClient ):
    service_name = "Logging"
    clientClass = oci.logging.LoggingManagementClient
    compositeClientClass = oci.logging.LoggingManagementClientCompositeOperations

    objects = [
        {
            "name_singular"      : "Agent Config",
            "name_plural"        : "Agent Configs",
            "function_list"      : "list_unified_agent_configurations",
            "function_delete"    : "delete_unified_agent_configuration",
        },

        {
            "name_singular"      : "Logging Group",
            "name_plural"        : "Logging Groups",
            "function_list"      : "list_log_groups",
            "function_delete"    : "delete_log_group",
        },
    ]

    def predelete(self,object,region,found_object):
        if "Logging Group" == object["name_singular"]:
            # then we need to delete the logs inside it first
            lgid = found_object.id
            logging.debug( "Getting logs in logging group {}".format(lgid))
            logs = self.clients[region].list_logs(lgid)
            logging.debug("Found {} logs in group".format(len(logs.data)))
            for l in logs.data:
                logging.debug("Deleting log id {}".format(l.id))
                self.compositeClients[region].delete_log_and_wait_for_state(lgid,l.id,["SUCCEEDED","FAILED"])

            return

        raise NotImplementedError

