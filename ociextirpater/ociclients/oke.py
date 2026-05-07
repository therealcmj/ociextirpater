import oci
from ociextirpater.OCIClient import OCIClient

class oke( OCIClient ):
    service_name = "OKE"
    clientClass = oci.container_engine.ContainerEngineClient
    compositeClientClass = oci.container_engine.container_engine_client_composite_operations.ContainerEngineClientCompositeOperations

    _kwargs_delete = {
                        "wait_for_states": [
                            oci.container_engine.models.WorkRequest.STATUS_SUCCEEDED,
                            oci.container_engine.models.WorkRequest.STATUS_FAILED,
                            ]
                    }

    objects = [
        {
            "name_singular"      : "OKE Cluster",
            "name_plural"        : "OKE Clusters",

            "formatter"          : lambda cluster: "OKE Cluster with OCID {} / name '{}' is in state {}".format(cluster.id, cluster.name, cluster.lifecycle_state),
            "function_list"      : "list_clusters",
            "kwargs_list"        : {
                                        "lifecycle_state": [
                                            "ACTIVE",
                                            "FAILED",
                                            "UPDATING"
                                        ]
                                   },
            "c_function_delete"  : "delete_cluster_and_wait_for_state",
            "kwargs_delete"      :  _kwargs_delete,
        },


        # {
        #     # "formatter"          : lambda instance: "XXX instance with OCID {} / name '{}' is in state {}".format( instance.id, instance.name, instance.lifecycle_state ),
        #     "function_list"      : "list_xxx",
        #     "kwargs_list"        : {
        #                            },
        #     "function_delete"    : "delete_xxx",
        #     "name_singular"      : "XXX",
        #     "name_plural"        : "XXXXs",
        # },
    ]
