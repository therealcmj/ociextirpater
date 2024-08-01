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

        {
            "function_list"      : "list_compartments",
            # "function_delete"    : "delete_compartment",
            "name_singular"      : "Compartment",
            "name_plural"        : "Compartments",
            "formatter"          : lambda compartment: "Compartment with OCID {} / name '{}' is in state {}".format(compartment.id,
                                                                                                                    compartment.name,
                                                                                                                    compartment.lifecycle_state),
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

    def predelete(self,object,region,found_object):
        self.compositeClients[region]
