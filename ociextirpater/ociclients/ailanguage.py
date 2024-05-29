import oci
from ociextirpater.OCIClient import OCIClient

class ailanguage( OCIClient ):
    service_name = "AI Language"
    clientClass = oci.ai_language.AIServiceLanguageClient

    objects = [
        {
            "name_singular"      : "Language Model",
            "name_plural"        : "Language Models",

            "function_list"      : "list_models",
            "function_delete"    : "delete_model",
        },

        {
            "name_singular"      : "Language Project",
            "name_plural"        : "Language Projects",

            "function_list"      : "list_projects",
            "function_delete"    : "delete_project",
        },

        {
            "name_singular"      : "Language Endpoint",
            "name_plural"        : "Language Endpoints",

            "function_list"      : "list_endpoints",
            "function_delete"    : "delete_endpoint",
        },

    ]
