import oci
from ociexterpater.OCIClient import OCIClient

class vision( OCIClient ):
    service_name = "AI Vision service"
    clientClass = oci.ai_vision.AIServiceVisionClient

    objects = [
        {
            # "function_list"    : "list_models",
            "kwargs_list"      : {
                                 },
            "function_delete"  : "delete_model",
            "name_singular"    : "AI Vision Model",
            "name_plural"      : "AI Vision Models"
        },
        {
            # "function_list"    : "list_projects",
            "kwargs_list"      : {
                                 },
            "function_delete"  : "delete_project",
            "name_singular"    : "AI Vision project",
            "name_plural"      : "AI Vision projects"
        },
    ]

    def list_objects(self, o, region, this_compartment, **kwargs):
        if o["name_plural"] == "AI Vision Models":
            return oci.pagination.list_call_get_all_results(
                getattr((self.clients[region]), "list_models"),
                **{"compartment_id":this_compartment}).data
        elif o["name_plural"] == "AI Vision projects":
            return oci.pagination.list_call_get_all_results(
                getattr((self.clients[region]), "list_projects"),
                **{"compartment_id": this_compartment}).data
        else:
            raise NotImplementedError
