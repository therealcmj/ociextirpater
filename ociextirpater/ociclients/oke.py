import oci
from ociextirpater.OCIClient import OCIClient

class oke( OCIClient ):
    service_name = "OKE"
    clientClass = oci.container_engine.ContainerEngineClient

    objects = [
        {
            "formatter"          : lambda cluster: "OKE Cluster with OCID {} / name '{}' is in state {}".format(cluster.id, cluster.name, cluster.lifecycle_state),
            "function_list"      : "list_clusters",
            "kwargs_list"        : {
                                        "lifecycle_state": [
                                            "ACTIVE",
                                            "FAILED",
                                            "UPDATING"
                                        ]
                                   },
            "function_delete"    : "delete_cluster",
            "name_singular"      : "OKE Cluster",
            "name_plural"        : "OKE Clusters",
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
