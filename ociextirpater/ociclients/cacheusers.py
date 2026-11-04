import oci
from ociextirpater.OCIClient import OCIClient


class cacheusers( OCIClient ):
    service_name = "Cache"
    clientClass = oci.redis.OciCacheUserClient

    objects = [
        {
            "name_singular"      : "OCI Cache user",
            "name_plural"        : "OCI Cache users",
            # "function_list"      : "list_oci_cache_users",
            "function_delete"    : "delete_oci_cache_user",
        },

    ]

    def list_objects(self, o, region, this_compartment, **kwargs):
        return oci.pagination.list_call_get_all_results(getattr((self.clients[region]), "list_oci_cache_users"),
                                                        **{"compartment_id": this_compartment}).data
