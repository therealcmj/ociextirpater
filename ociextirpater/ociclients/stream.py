import oci
from ociextirpater.OCIClient import OCIClient

class stream( OCIClient ):
    service_name = "Stream Pool"
    clientClass = oci.streaming.StreamAdminClient
    compositeClientClass = oci.streaming.StreamAdminClientCompositeOperations

    objects = [
        {
            "name_singular"      : "Stream",
            "name_plural"        : "Streams",

            "function_list"      : "list_streams",
            "formatter"          : lambda pool: "Stream pool with OCID {} / name '{}' is in state {}".format( pool.id,
                                                                                                              pool.name,
                                                                                                              pool.lifecycle_state ),

            "c_function_delete"  : "delete_stream_and_wait_for_state",
            "kwargs_delete"      : {
                                    "wait_for_states": ["DELETED"]
                                   }
        },

        {
            "name_singular"      : "Stream Pool",
            "name_plural"        : "Stream Pools",

            "function_list"      : "list_stream_pools",
            "formatter"          : lambda pool: "Stream pool with OCID {} / name '{}' is in state {}".format( pool.id,
                                                                                                              pool.name,
                                                                                                              pool.lifecycle_state ),
            "function_delete"    : "delete_stream_pool",
        },

        {
            "name_singular"      : "Connect Harness",
            "name_plural"        : "Connect Harnesses",
            "function_list"      : "list_connect_harnesses",
            "formatter"          : lambda harness: "Connect Harness with OCID {} / name '{}' is in state {}".format(harness.id, harness.name, harness.lifecycle_state),

            "function_delete"    : "delete_connect_harness",
        },

    ]


    def list_objects(self, o, region, this_compartment, **kwargs):
        if o["name_plural"] == "Streams":
            return oci.pagination.list_call_get_all_results(
                getattr((self.clients[region]), "list_streams"), **{"compartment_id":this_compartment}).data
        else:
            raise NotImplementedError
