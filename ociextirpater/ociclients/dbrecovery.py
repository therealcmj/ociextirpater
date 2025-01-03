import oci
from ociextirpater.OCIClient import OCIClient

class dbrecovery( OCIClient ):
    service_name = "DB Recovery"
    clientClass = oci.recovery.DatabaseRecoveryClient

    objects = [

        {
            "name_singular"      : "Protected Database",
            "name_plural"        : "Protected Databases",

            "function_list"      : "list_protected_databases",
            "function_delete"    : "delete_protected_database",
        },

        {
            "name_singular"      : "Protection Policy",
            "name_plural"        : "list_protection_policies",
            # don't try to delete pre-defined policies
            "check2delete"       : lambda policy: False == policy.is_predefined_policy,
            "function_list"      : "list_protection_policies",
            "kwargs_list"        : {
                                        "lifecycle_state": "ACTIVE"
                                   },
            "function_delete"    : "delete_protection_policy",
        },

        {
            "name_singular"      : "Recovery Service Subnet",
            "name_plural"        : "Recovery Service Subnets",
            "function_list"      : "list_recovery_service_subnets",
            "kwargs_list"        : {
                                        "lifecycle_state": "ACTIVE"
                                   },
            "function_delete"    : "delete_recovery_service_subnet",
        },
    ]
