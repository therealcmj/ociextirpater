import oci
from ociexterpater.OCIClient import OCIClient

class logging( OCIClient ):
    service_name = "Logging"
    clientClass = oci.logging.LoggingManagementClient

    objects = [
        {
            "function_list"      : "list_log_groups",
            "function_delete"    : "delete_log_group",
            "name_singular"      : "Logging Group",
            "name_plural"        : "Logging Groups",
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
        pass
