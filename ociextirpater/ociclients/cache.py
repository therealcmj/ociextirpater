import oci
from ociextirpater.OCIClient import OCIClient

class cache( OCIClient ):
    service_name = "Cache"
    clientClass = oci.redis.RedisClusterClient

    objects = [
        {
            "name_singular"      : "OCI Cache (Redis) cluster",
            "name_plural"        : "OCI Cache (Redis) clusters",
            "function_delete"    : "delete_redis_cluster",
        }
    ]

    def list_objects(self, o, region, this_compartment, **kwargs):
        return oci.pagination.list_call_get_all_results(getattr((self.clients[region]), "list_redis_clusters"),
                                                        **{"compartment_id": this_compartment}).data
