import logging
import socket
from urllib.parse import urlsplit
import oci
from oci.retry import RetryStrategyBuilder
from ociextirpater.OCIClient import OCIClient

class genaiclient( OCIClient ):
    service_name = "Generative AI Client"
    clientClass = oci.generative_ai.generative_ai_client.GenerativeAiClient
    # clientClass = oci.identity.identity_client.IdentityClient
    compositeClientClass = oci.generative_ai.generative_ai_client_composite_operations.GenerativeAiClientCompositeOperations

    # TODO: go through and figure out which function_delete's need to be changed to c_
    # to allow the cluster delete to succeed immediately
    objects = [
        {
            "name_singular"      : "API Key",
            "name_plural"        : "API Keys",
            "function_list"      : "list_api_keys",
            "function_delete"    : "delete_api_key",            
        },

        {
            "name_singular"      : "Endpoint",
            "name_plural"        : "Endpoints",
            "function_list"      : "list_endpoints",
            "list_kwargs"        : {"lifecycle_state": oci.generative_ai.models.Endpoint.LIFECYCLE_STATE_ACTIVE},
            # "function_delete"    : "delete_endpoint",
            "c_function_delete"  : "delete_endpoint_and_wait_for_state",
            "function_delete_args" : {
                "wait_for_states": [
                    oci.generative_ai.models.WorkRequest.STATUS_SUCCEEDED,
                    oci.generative_ai.models.WorkRequest.STATUS_FAILED],
                    # "max_wait_seconds": 1200
                }
        },

        {
            "name_singular"      : "Private Endpoint",
            "name_plural"        : "Private Endpoints",
            "function_list"      : "list_generative_ai_private_endpoints",
            "function_delete"    : "delete_generative_ai_private_endpoint",
        },

        {
            "name_singular"      : "Project",
            "name_plural"        : "Projects",
            "function_list"      : "list_generative_ai_projects",
            "function_delete"    : "delete_generative_ai_project",
        },

        {
            "name_singular"      : "Hosted Application Storage",
            "name_plural"        : "Hosted Application Storage",
            "function_list"      : "list_hosted_application_storage",
            "function_delete"    : "delete_hosted_application_storage",
        },

        {
            "name_singular"      : "Hosted Application",
            "name_plural"        : "Hosted Applications",
            "function_list"      : "list_hosted_applications",
            "kwargs_list"        : {"lifecycle_state": oci.generative_ai.models.HostedApplication.LIFECYCLE_STATE_ACTIVE},
            "function_delete"    : "delete_hosted_application",
        },

        {
            "name_singular"      : "Hosted Deployment",
            "name_plural"        : "Hosted Deployments",
            "function_list"      : "list_hosted_deployments",
            "function_delete"    : "delete_hosted_deployment",
        },

        {
            "name_singular"      : "Imported Model",
            "name_plural"        : "Imported Models",
            "function_list"      : "list_imported_models",
            "function_delete"    : "delete_imported_model",
        },

        {
            "name_singular"      : "Dedicated AI Cluster",
            "name_plural"        : "Dedicated AI Clusters",
            "function_list"      : "list_dedicated_ai_clusters",
            "kwargs_list"        : {"lifecycle_state": oci.generative_ai.models.DedicatedAiCluster.LIFECYCLE_STATE_ACTIVE},
            "function_delete"    : "delete_dedicated_ai_cluster",
        },

        {
            "name_singular"      : "Semantic Store",
            "name_plural"        : "Semantic Stores",
            "function_list"      : "list_semantic_stores",
            # TODO: implement the search here 
            "function_delete"    : "delete_semantic_store"
        },

        {
            "name_singular"      : "Vector Store Connector File Sync",
            "name_plural"        : "Vector Store Connector File Syncs",
            "function_list"      : "list_vector_store_connector_file_syncs",
            "function_delete"    : "delete_vector_store_connector_file_sync",
        },

        {
            "name_singular"      : "Vector Store Connector",
            "name_plural"        : "Vector Store Connector",
            "function_list"      : "list_vector_store_connectors",
            "kwargs_list"        : {"lifecycle_state": oci.generative_ai.models.VectorStoreConnector.LIFECYCLE_STATE_ACTIVE},
            "function_delete"    : "delete_vector_store_connector",
        }
    ]

    def __init__(self,config):
        # from oci.retry import NoneRetryStrategy, retry_checkers
        super().__init__(config)

        rs = RetryStrategyBuilder().add_max_attempts(max_attempts=1) \
            .add_total_elapsed_time(total_elapsed_time_seconds=10) \
            .get_retry_strategy()
            # .add_service_error_check(service_error_retry_config=retry_checkers.RETRYABLE_STATUSES_AND_CODES,
            #                         service_error_retry_on_any_5xx=False) \

        tenant_id = config.ociconfig['tenancy']
        for k in sorted(list(self.clients.keys())):
            logging.debug("Checking service availability in region {}".format(k))
            try:
                client = self.clients[k]
                # o = urlsplit(client.base_client._endpoint)
                # and then get the hostname out
                # hn = o.hostname
                # logging.debug("Attempting to resolve hostname {} for service in region {}".format(hn, k))
                # ip = socket.gethostbyname(hn)

                f = getattr(client, "list_work_requests", {"retry_strategy": rs})
                logging.debug("Calling list_work_requests for region {} to check service availability".format(k))
                response = f(tenant_id, limit=1)
                if response.status != 200:
                    raise Exception("Non-200 response")
                else:
                    logging.info("Service appears to be available in region {}".format(k))
            except Exception as e:
                logging.info("Service does NOT appear to be available in region {}. That region will be skipped".format(k))
                self.clients.pop(k)

        logging.debug("Finished checking service availability in regions. Final regions with service available: {}".format(list(self.clients.keys())))



    def delete_object(self, object, region, found_object):
        if object["name_plural"] == "'Dedicated AI Clusters'":
            # TODO: see if there are any remaining 
            pass
            
        return super().delete_object(object, region, found_object)