import oci
from ociextirpater.OCIClient import OCIClient

class apiplan( OCIClient ):
    service_name = "API Plan"
    clientClass = oci.apigateway.UsagePlansClient
    compositeClientClass = oci.apigateway.UsagePlansClientCompositeOperations

    objects = [
        {
            "name_singular"      : "Usage Plan",
            "name_plural"        : "Usage Plans",
            "function_list"      : "list_usage_plans",
            "function_delete"    : "delete_usage_plan",
            # "c_function_delete"  : "delete_usage_plan_and_wait_for_state"
        },

    ]
