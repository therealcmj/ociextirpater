import oci
from ociextirpater.OCIClient import OCIClient

class datalabeling( OCIClient ):
    service_name = "Data Labeling"
    clientClass = oci.data_labeling_service.DataLabelingManagementClient

    objects = [
        {
            "name_singular"      : "Data Set",
            "name_plural"        : "Data Sets",
            "function_list"      : "list_datasets",
            "function_delete"    : "delete_dataset",
        },
    ]
