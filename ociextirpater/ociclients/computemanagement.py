import oci
from ociextirpater.OCIClient import OCIClient

class computemanagement( OCIClient ):
    service_name = "Compute Managament"
    clientClass = oci.core.ComputeManagementClient

    objects = [
        {
            "name_singular"      : "Instance Pool",
            "name_plural"        : "Instance Pools",

            "function_list"      : "list_instance_pools",
            "function_delete"    : "delete_instance_pool",
        },

        {
            "name_singular"      : "Instance Configuration",
            "name_plural"        : "Instance Configurations",

            "function_list"      : "list_instance_configurations",
            "function_delete"    : "delete_instance_configuration",
            "formatter"          : lambda instanceconfig: "Instance Config with OCID {} / name '{}'".format(instanceconfig.id, instanceconfig.display_name),
        },
    ]
