import logging
import oci
from ociextirpater.OCIClient import OCIClient

class apideployment( OCIClient ):
    service_name = "API Deployment"
    clientClass = oci.apigateway.deployment_client.DeploymentClient
    # compositeClientClass = oci.apigateway.deployment_client_composite_operations.DeploymentClientCompositeOperations

    objects = [
        {
            "name_singular"      : "Deployment",
            "name_plural"        : "Deployments",
            "function_list"      : "list_deployments",
            "function_get"       : "get_deployment",
            "function_delete"    : "delete_deployment",
            # "c_function_delete"  : "delete_deployment_and_wait_for_state",
        },
    ]

    def delete_object(self, object, region, found_object):
        if object["name_singular"] == "Deployment":
            # APIGW-53294
            # f = getattr(self.compositeClients[region], object["c_function_delete"])
            # f( 
            #     deployment_id=found_object.id,
            #     wait_for_states=[
            #                         oci.apigateway.models.WorkRequest.STATUS_SUCCEEDED,
            #                         oci.apigateway.models.WorkRequest.STATUS_FAILED,
            #                     ]
            # )
            # return

            f = getattr(self.clients[region], object["function_delete"])
            logging.debug("Calling delete function")
            f( deployment_id=found_object.id )
            oci.wait_until(
                self.clients[region],
                self.clients[region].get_deployment(deployment_id=found_object.id),
                evaluate_response=lambda r: r.data.lifecycle_state == oci.apigateway.models.Deployment.LIFECYCLE_STATE_DELETED,
            )
            logging.debug("Delete of deployment complete")
            return


        super().delete_object(object)

