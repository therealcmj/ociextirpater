import oci
from ociextirpater.OCIClient import OCIClient

class identity( OCIClient ):
    service_name = "Identity"
    clientClass = oci.identity.IdentityClient
    compositeClientClass = oci.identity.IdentityClientCompositeOperations

    isRegional = False

    objects = [
        {
            "name_singular"      : "Policy",
            "name_plural"        : "Policies",

            "function_list"      : "list_policies",
            "function_delete"    : "delete_policy",
            "formatter"          : lambda policy: "Policy with OCID {} / name '{}' is in state {}".format(policy.id,policy.name,policy.lifecycle_state),
        },
    ]

