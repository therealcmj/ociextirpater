import logging
import oci
from ociextirpater.OCIClient import OCIClient

class aidp( OCIClient ):
    service_name = "AI Data Platform"
    clientClass = oci.ai_data_platform.AiDataPlatformClient

    objects = [
        {
            "name_singular"      : "AI Data Platform",
            "name_plural"        : "AI Data Platforms",

            # AIDP passes the compartment ID in as a kwarg
            # "function_list"      : "list_ai_data_platforms",

            # delete needs a special argument to "force" deletion.
            # "function_delete"    : "delete_ai_data_platform",
        },

    ]

    def findAllInCompartment(self, region, o, this_compartment, **kwargs):
        if o["name_plural"] == "AI Data Platforms":
            return oci.pagination.list_call_get_all_results(
                getattr((self.clients[region]), "list_ai_data_platforms"),
                **{"compartment_id":this_compartment,"include_legacy":True}).data

        raise NotImplementedError


    def delete_object(self, object, region, found_object):
        logging.debug("Deleting with delete_object implementation in aidp class")
        self.clients[region].delete_ai_data_platform(found_object.id, **{"is_force_delete": True})

