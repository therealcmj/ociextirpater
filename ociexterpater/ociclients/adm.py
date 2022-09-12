import oci
from ociexterpater.OCIClient import OCIClient

class adm( OCIClient ):
    service_name = "Application Dependency Management service"
    clientClass = oci.adm.ApplicationDependencyManagementClient

    objects = [
        {
            # "function_list"    : "list_vulnerability_audits",
            "function_delete"  : "delete_vulnerability_audit",
            "name_singular"    : "ADM Vulnerability Audit",
            "name_plural"      : "ADM Vulnerability Audits"
        },
        {
            # "function_list": "list_knowledge_bases",
            "function_delete": "delete_knowledge_base",
            "name_singular": "ADM Knowledge Base",
            "name_plural": "ADM Knowledge Bases"
        }
    ]

    def list_objects(self, o, region, this_compartment, **kwargs):
        if o["name_plural"] == "ADM Vulnerability Audits":
            return oci.pagination.list_call_get_all_results(    getattr((self.clients[region]), "list_vulnerability_audits"),
                                                                **{"compartment_id":this_compartment}).data
        elif o["name_plural"] == "ADM Knowledge Bases":
            return oci.pagination.list_call_get_all_results(
                getattr((self.clients[region]), "list_knowledge_bases"),
                **{"compartment_id": this_compartment}).data
        else:
            raise NotImplementedError

