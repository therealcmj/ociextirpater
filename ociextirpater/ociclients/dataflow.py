import logging
import oci
from ociextirpater.OCIClient import OCIClient

class dataflow( OCIClient ):
    service_name = "Data Flow"
    clientClass = oci.data_flow.DataFlowClient
    compositeClientClass = oci.data_flow.DataFlowClientCompositeOperations

    objects = [
        {
            "name_singular"      : "Run",
            "name_plural"        : "Runs",
            "function_list"      : "list_runs",
            "check2delete"       : lambda run: run.lifecycle_state != "FAILED",
            "function_delete"    : "delete_run",
        },

        {
            "name_singular"      : "Application",
            "name_plural"        : "Applications",
            "function_list"      : "list_applications",
            "function_delete"    : "delete_application",
        },

        {
            "name_singular"      : "Pool",
            "name_plural"        : "Pools",
            "function_list"      : "list_pools",
            "function_delete"    : "delete_pool",
        },

        {
            "name_singular"      : "Private Endpoint",
            "name_plural"        : "Private Endpoints",
            "function_list"      : "list_private_endpoints",
            "function_delete"    : "delete_private_endpoint",
        },

    ]


    def predelete(self,object,region,found_object):
        if object["name_plural"] == "Pools":
            # anything that is not stopped needs to be stopped before it can be deleted.
            logging.info("Pool is currently in lifecycle state {}".format(found_object.lifecycle_state))
            if found_object.lifecycle_state != found_object.LIFECYCLE_STATE_STOPPED:
                logging.info("Stopping")
                
                # f = getattr((self.compositeClients[region]), "stop_pool_and_wait_for_state")
                # f( 
                #     found_object.id,
                #     wait_for_states=[ 
                #         oci.data_flow.models.WorkRequest.STATUS_SUCCEEDED
                #         ]
                # )

                f = getattr((self.clients[region]), "stop_pool")
                f(found_object.id)

                logging.debug("Waiting for data flow pool to stop")
                oci.waiter.wait_until(
                    self.clients[region],
                    self.clients[region].get_pool(found_object.id),
                    evaluate_response=lambda r: r.data.lifecycle_state == oci.data_flow.models.Pool.LIFECYCLE_STATE_STOPPED,
                    max_wait_seconds=1200
                )

                logging.info("Pool stopped and now ready for deletion")
                return
                
        raise NotImplementedError
