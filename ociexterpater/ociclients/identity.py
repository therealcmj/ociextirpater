import oci
from ociexterpater.OCIClient import OCIClient

class identity( OCIClient ):
    service_name = "Identity"
    clientClass = oci.identity.IdentityClient
    compositeClientClass = oci.identity.IdentityClientCompositeOperations

    isRegional = False

    objects = [
        {
            "function_list"      : "list_compartments",
            # "function_delete"    : "delete_compartment",
            "name_singular"      : "Compartment",
            "name_plural"        : "Compartments",
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
