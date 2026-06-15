import oci
from ociextirpater.OCIClient import OCIClient

class apigateway( OCIClient ):
    service_name = "API Gateway"
    clientClass = oci.apigateway.GatewayClient

    objects = [
        {
            "name_singular"      : "API Gateway",
            "name_plural"        : "API Gateways",
            "function_list"      : "list_gateways",
            "function_get"       : "get_gateway",
            "function_delete"    : "delete_gateway",
        },
    ]
