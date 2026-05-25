import oci
from ociextirpater.OCIClient import OCIClient

class bigdata( OCIClient ):
    service_name = "BigData"
    clientClass = oci.bds.BdsClient
    compositeClientClass = oci.bds.BdsClientCompositeOperations

    objects = [
        {
            "name_singular"      : "Instance",
            "name_plural"        : "Instances",
            "function_list"      : "list_bds_instances",
            "function_delete"    : "delete_bds_instance",
        },
    ]
