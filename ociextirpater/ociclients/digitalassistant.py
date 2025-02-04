import logging
import oci
from ociextirpater.OCIClient import OCIClient

class digitalassistant( OCIClient ):
    service_name = "Digital Assistant"
    clientClass = oci.oda.OdaClient

    objects = [
        {
            "name_singular"      : "Digital Assistant Instance",
            "name_plural"        : "Digital Assistant Instances",
            "function_list"      : "list_oda_instances",
            "function_delete"    : "delete_oda_instance",
        },
    ]
