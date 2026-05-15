import oci
from ociextirpater.OCIClient import OCIClient

class aivision( OCIClient ):
    service_name = "AI Vision"
    clientClass = oci.ai_vision.AIServiceVisionClient
    compositeClientClass = oci.ai_vision.AIServiceVisionClientCompositeOperations

    _kwargs_delete_wait = {
                        "wait_for_states": [
                            oci.ai_vision.models.WorkRequest.STATUS_SUCCEEDED,
                            oci.ai_vision.models.WorkRequest.STATUS_FAILED,
                            ]
                    }

    objects = [
        {
            "name_singular"      : "Vision Model",
            "name_plural"        : "Vision Models",
            "function_list"      : "list_models",
            # delete and wait so that we can delete the project later
            "c_function_delete"  : "delete_model_and_wait_for_state",
            "kwargs_delete"      :  _kwargs_delete_wait,
        },

        {
            "name_singular"      : "Vision Project",
            "name_plural"        : "Vision Projects",
            "function_list"      : "list_projects",
            "function_delete"    : "delete_project",
        },

        {
            "name_singular"      : "Vision Private Endpoint",
            "name_plural"        : "Vision Private Endpoints",
            "function_list"      : "list_vision_private_endpoints",
            "function_delete"    : "delete_vision_private_endpoint",
        },

        {
            "name_singular"      : "Vision Stream Group",
            "name_plural"        : "Vision Stream Groups",
            "function_list"      : "list_stream_groups",
            "function_delete"    : "delete_stream_group",
        },

        {
            "name_singular"      : "Vision Stream Job",
            "name_plural"        : "Vision Stream Jobs",
            "function_list"      : "list_stream_jobs",
            "function_delete"    : "delete_stream_job",
        }

    ]


    def list_objects(self, o, region, this_compartment, **kwargs):
        # a careful programmer looks both ways before crossing the street. But since I'm the only coder here YOLO
        # o.get() will throw an exception if function_list is missing. Which is a good enough check for now
        function_name = o.get("function_list", None)
        return oci.pagination.list_call_get_all_results(
            getattr((self.clients[region]), function_name),
            **{"compartment_id":this_compartment}
        ).data
