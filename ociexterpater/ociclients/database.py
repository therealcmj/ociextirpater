import oci
from ociexterpater.OCIClient import OCIClient

class database( OCIClient ):
    service_name = "Database"
    clientClass = oci.database.DatabaseClient

    objects = [
        # {
        #     "function_list"      : "list_autonomous_databases",
        #     "function_delete"    : "delete_autonomous_database",
        #     "name_singular"      : "Autonomous Database",
        #     "name_plural"        : "Autonomous Databases",
        # },
        #
        # {
        #     # "function_list"      : "list_backups",
        #     "function_delete"    : "delete_backup",
        #     "name_singular"      : "Database Backup",
        #     "name_plural"        : "Database Backups",
        # },
        #
        # {
        #     "function_list"      : "list_backup_destinations",
        #     "function_delete"    : "delete_backup_destination",
        #     "name_singular"      : "Database Backup Destination",
        #     "name_plural"        : "Database Backup Destinations",
        # },

        {
            "function_list"      : "list_db_homes",
            "function_delete"    : "delete_db_home",
            "name_singular"      : "Database home",
            "name_plural"        : "Database homes",
        },

        # {
        #     # "function_list"      : "list_databases",
        #     "function_delete"    : "delete_database",
        #     "name_singular"      : "Database",
        #     "name_plural"        : "Databases",
        # },

        # {
        #     # "formatter"          : lambda instance: "XXX instance with OCID {} / name '{}' is in state {}".format( instance.id, instance.name, instance.lifecycle_state ),
        #     "function_list"      : "list_xxx",
        #     "function_delete"    : "delete_xxx",
        #     "name_singular"      : "XXX",
        #     "name_plural"        : "XXXXs",
        # },
    ]


    def list_objects(self, o, region, this_compartment, **kwargs):
        if o["name_plural"] == "Database Backups":
            return oci.pagination.list_call_get_all_results(
                getattr((self.clients[region]), "list_backups"),
                **{"compartment_id":this_compartment}).data

        # if o["name_plural"] == "Databases":
        #     return oci.pagination.list_call_get_all_results(
        #         getattr((self.clients[region]), "list_databases"),
        #         **{
        #             "compartment_id": this_compartment,
        #             "lifecycle_state": "AVAILABLE"
        #         }).data

        raise NotImplementedError
