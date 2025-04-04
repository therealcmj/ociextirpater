import logging
import oci
from ociextirpater.OCIClient import OCIClient

class dbmigration( OCIClient ):
    service_name = "Database Migration"
    clientClass = oci.database_migration.DatabaseMigrationClient
    compositeClientClass = oci.database_migration.DatabaseMigrationClientCompositeOperations

    objects = [
        {
            "name_singular"      : "Migration",
            "name_plural"        : "Migrations",
            "function_list"      : "list_migrations",
            # "function_delete"    : "delete_migration",
            "c_function_delete"  : "delete_migration_and_wait_for_state",
            "kwargs_delete"      :  {
                                        "wait_for_states": oci.database_migration.models.WorkRequest.STATUS_SUCCEEDED
                                    }
        },

        {
            "name_singular"      : "Connection",
            "name_plural"        : "Connections",
            "function_list"      : "list_connections",
            "function_delete"    : "delete_connection",
        },
    ]
