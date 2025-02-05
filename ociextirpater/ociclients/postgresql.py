import logging
import oci
from ociextirpater.OCIClient import OCIClient

class postgresql( OCIClient ):
    service_name = "PostgreSQL"
    clientClass = oci.psql.PostgresqlClient

    objects = [
        {
            "name_singular"      : "Backup",
            "name_plural"        : "Backups",
            "function_list"      : "list_backups",
            "function_delete"    : "delete_backup",
        },

        {
            "name_singular"      : "Configuration",
            "name_plural"        : "Configurations",
            "function_list"      : "list_configurations",
            "function_delete"    : "delete_configuration",
        },

        {
            "name_singular"      : "DB System",
            "name_plural"        : "DB Systems",
            "function_list"      : "list_db_systems",
            "function_delete"    : "delete_db_system",
        },

    ]


    # overriding the OCIClient:list_objects() method
    # because the postgresql control plane APIs use the **kwargs pattern
    def list_objects(self, o, region, this_compartment, **kwargs):
        return oci.pagination.list_call_get_all_results(
            getattr((self.clients[region]), o["function_list"]),
            **{"compartment_id": this_compartment}
        ).data
