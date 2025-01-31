import logging
import oci
from ociextirpater.OCIClient import OCIClient

class api( OCIClient ):
    service_name = "API"
    clientClass = oci.apigateway.api_gateway_client.ApiGatewayClient

    objects = [
        {
            "name_singular"      : "API",
            "name_plural"        : "APIs",
            "function_list"      : "list_apis",
            "function_delete"    : "delete_api",
        },
    ]
