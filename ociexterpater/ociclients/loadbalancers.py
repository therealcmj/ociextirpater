import oci
from ociexterpater.OCIClient import OCIClient

class loadbalancers( OCIClient ):
    service_name = "Load Balancers"
    clientClass = oci.load_balancer.LoadBalancerClient

    objects = [
        {
            # "formatter"          : lambda instance: "XXX instance with OCID {} / name '{}' is in state {}".format( instance.id, instance.name, instance.lifecycle_state ),
            "function_list"      : "list_load_balancers",
            "function_delete"    : "delete_load_balancer",
            "name_singular"      : "Load Balancer",
            "name_plural"        : "Load Balancers",
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
