import oci
from ociexterpater.OCIClient import OCIClient

class anomaly( OCIClient ):
    service_name = "Anomaly Detection service"
    clientClass = oci.ai_anomaly_detection.AnomalyDetectionClient

    objects = [
        {
            "function_list"    : "list_data_assets",
            "kwargs_list"      : {
                                 },
            "function_delete"  : "delete_data_asset",
            "name_singular"    : "AI Anomaly Data Asset",
            "name_plural"      : "AI Anomaly Data Asset"
        },
        {
            "function_list"    : "list_ai_private_endpoints",
            "kwargs_list"      : {
                                 },
            "function_delete"  : "delete_ai_private_endpoint",
            "name_singular"    : "AI Anomaly Private Endpoint",
            "name_plural"      : "AI Anomaly Private Endpoint"
        },
        {
            "function_list"    : "list_models",
            "kwargs_list"      : {
                                 },
            "function_delete"  : "delete_model",
            "name_singular"    : "AI Anomaly Model",
            "name_plural"      : "AI Anomaly Models"
        },
        {
            "function_list"    : "list_projects",
            "kwargs_list"      : {
                                 },
            "function_delete"  : "delete_project",
            "name_singular"    : "AI Anomaly project",
            "name_plural"      : "AI Anomaly project"
        },
    ]
