import oci
from ociextirpater.OCIClient import OCIClient

class aianomaly( OCIClient ):
    service_name = "AI Anomaly Detection"
    clientClass = oci.ai_anomaly_detection.AnomalyDetectionClient

    objects = [
        {
            "name_singular"      : "AI Anomaly Project",
            "name_plural"        : "AI Anomaly Projects",

            "function_list"      : "list_projects",
            "function_delete"    : "delete_project",
        },

        {
            "name_singular"      : "AI Anomaly Model",
            "name_plural"        : "AI Anomaly Models",

            "function_list"      : "list_models",
            "function_delete"    : "delete_model",
        },

        {
            "name_singular"      : "AI Anomaly Data Asset",
            "name_plural"        : "AI Anomaly Data Assets",

            "function_list"      : "list_data_assets",
            "function_delete"    : "delete_data_asset",
        },

        {
            "name_singular"      : "AI Anomaly Private Endpoint",
            "name_plural"        : "AI Anomaly Private Endpoints",

            "function_list"      : "list_ai_private_endpoints",
            "function_delete"    : "delete_ai_private_endpoint",
        },

    ]
