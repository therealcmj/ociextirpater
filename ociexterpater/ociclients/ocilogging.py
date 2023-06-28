import logging
import oci
from ociexterpater.OCIClient import OCIClient

class ocilogging( OCIClient ):
    service_name = "Logging"
    clientClass = oci.logging.LoggingManagementClient
    compositeClientClass = oci.logging.LoggingManagementClientCompositeOperations

    objects = [
        {
            "function_list"      : "list_log_groups",
            "function_delete"    : "delete_log_group",
            "name_singular"      : "Logging Group",
            "name_plural"        : "Logging Groups",
        },

        # {
        #     # "formatter"          : lambda instance: "XXX instance with OCID {} / name '{}' is in state {}".format( instance.id, instance.name, instance.lifecycle_state ),
        #     "function_list"      : "list_xxx",
        #     "kwargs_list"        : {
        #                            },
        #     "function_delete"    : "delete_xxx",
        #     "name_singular"      : "XXX",
        #     "name_plural"        : "XXXXs",
        # },
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
                self.compositeClients[region].delete_log_and_wait_for_state(lgid,l.id,["SUCCEEDED"])
