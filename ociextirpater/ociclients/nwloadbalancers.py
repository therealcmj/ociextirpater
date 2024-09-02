import oci
from ociextirpater.OCIClient import OCIClient

class nwloadbalancers( OCIClient ):
    service_name = "Network Load Balancers"
    clientClass = oci.network_load_balancer.NetworkLoadBalancerClient

    objects = [
        {
            "name_singular"      : "Network Load Balancer",
            "name_plural"        : "Network Load Balancers",
            "function_list"      : "list_network_load_balancers",
            "function_delete"    : "delete_network_load_balancer",
        },
    ]
