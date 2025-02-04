import logging
import oci
from ociextirpater.OCIClient import OCIClient

class goldengate( OCIClient ):
    service_name = "GoldenGate"
    clientClass = oci.golden_gate.GoldenGateClient

    objects = [
        {
            "name_singular"      : "Connection Assignment",
            "name_plural"        : "Connection Assignments",
            "function_list"      : "list_connection_assignments",
            "formatter"          : lambda ca: "Connection Assignment with OCID {} / alias name '{}' is in state {}".format(ca.id, ca.alias_name, ca.lifecycle_state),
            "function_delete"    : "delete_connection_assignment",

        },

        {
            "name_singular"      : "Connection",
            "name_plural"        : "Connections",
            "function_list"      : "list_connections",
            "function_delete"    : "delete_connection",
        },


        {
            "name_singular"      : "Database Registration",
            "name_plural"        : "Database Registrations",
            "function_list"      : "list_database_registrations",
            "function_delete"    : "delete_database_registration",
        },


        {
            "name_singular"      : "Deployment Backup",
            "name_plural"        : "Deployment Backups",
            "function_list"      : "list_deployment_backups",
            "check2delete"       : lambda backup: hasattr(backup, "is_automatic") and backup.is_automatic != True,

            "function_delete"    : "delete_deployment_backup",
        },

        {
            "name_singular"      : "Deployment",
            "name_plural"        : "Deployments",
            "function_list"      : "list_deployments",
            "function_delete"    : "delete_deployment",
        },


    ]
