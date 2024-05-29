import oci
from ociextirpater.OCIClient import OCIClient

class aidocument( OCIClient ):
    service_name = "AI Document"
    clientClass = oci.ai_document.AIServiceDocumentClient

    objects = [
        {
            "name_singular"      : "Document Project",
            "name_plural"        : "Document Projects",
            "function_delete"    : "delete_project",
        },

    ]


    def list_objects(self, o, region, this_compartment, **kwargs):
        if o["name_plural"] == "Document Projects":
            return oci.pagination.list_call_get_all_results(
                getattr((self.clients[region]), "list_projects"),
                **{"compartment_id":this_compartment}
            ).data
