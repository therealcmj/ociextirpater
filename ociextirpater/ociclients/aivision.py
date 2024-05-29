import oci
from ociextirpater.OCIClient import OCIClient

class aivision( OCIClient ):
    service_name = "AI Speech"
    clientClass = oci.ai_vision.AIServiceVisionClient

    objects = [
        {
            "name_singular"      : "Vision Model",
            "name_plural"        : "Vision Models",
            "function_delete"    : "delete_model",
        },

        {
            "name_singular": "Vision Project",
            "name_plural": "Vision Projects",
            "function_delete": "delete_project",
        },
    ]


    def list_objects(self, o, region, this_compartment, **kwargs):
        if o["name_plural"] == "Vision Models":
            return oci.pagination.list_call_get_all_results(
                getattr((self.clients[region]), "list_models"),
                **{"compartment_id":this_compartment}
            ).data
        if o["name_plural"] == "Vision Projects":
            return oci.pagination.list_call_get_all_results(
                getattr((self.clients[region]), "list_projects"),
                **{"compartment_id":this_compartment}
            ).data
