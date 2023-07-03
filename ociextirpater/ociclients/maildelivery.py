import oci
from ociextirpater.OCIClient import OCIClient

class maildelivery( OCIClient ):
    service_name = "Mail Delivery"
    clientClass = oci.email.EmailClient

    objects = [
        {
            "name_singular": "Email Sender",
            "name_plural": "Email Senders",

            "function_list": "list_senders",
            "kwargs_list": {
                "lifecycle_state": "ACTIVE"
            },
            "formatter": lambda sender: "Email Sender with OCID {} / address '{}' is in state {}".format(sender.id,
                                                                                                         sender.email_address,
                                                                                                         sender.lifecycle_state),
            "function_delete": "delete_sender",
        },

        {
            "name_singular"      : "Email Domain",
            "name_plural"        : "Email Domains",

            "function_list"      : "list_email_domains",
            "function_delete"    : "delete_email_domain",
        },


        # {
        #     "name_singular"      : "Suppression",
        #     "name_plural"        : "Suppressions",
        #     "function_list"      : "list_suppressions",
        #     "function_delete"    : "delete_suppression",
        # }

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
