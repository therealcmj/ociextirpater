import oci
from ociextirpater.OCIClient import OCIClient

class serviceconnector( OCIClient ):
    service_name = "Service Connector"
    clientClass = oci.sch.ServiceConnectorClient

    objects = [
        {
            "name_singular"      : "Service Connector",
            "name_plural"        : "Service Connectors",

            "function_list"      : "list_service_connectors",
            "function_delete"    : "delete_service_connector",
        },

    ]
