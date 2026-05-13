import logging
import oci
from ociextirpater.OCIClient import OCIClient

class opa( OCIClient ):
    service_name = "Process Automation"
    clientClass = oci.opa.opa_instance_client.OpaInstanceClient

    objects = [
        {
            "name_singular"      : "Process Automation Instance",
            "name_plural"        : "Process Automation Instances",
            "function_list"      : "list_opa_instances",
            "function_delete"    : "delete_opa_instance",
        }
    ]

    def list_objects(self, o, region, this_compartment, **kwargs):
        function_name = o.get("function_list", None)
        if function_name is not None:
            return oci.pagination.list_call_get_all_results(
                getattr((self.clients[region]), function_name),
                **{"compartment_id":this_compartment}
            ).data
        else:
            return []
