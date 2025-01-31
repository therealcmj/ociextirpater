import logging
import oci
from ociextirpater.OCIClient import OCIClient

class apideployment( OCIClient ):
    service_name = "API Deployment"
    clientClass = oci.apigateway.deployment_client.DeploymentClient

    objects = [
        {
            "name_singular"      : "Deployment Client",
            "name_plural"        : "Deployment Clients",
            "function_list"      : "list_deployments",
            "function_delete"    : "delete_deployment",
        },
    ]
