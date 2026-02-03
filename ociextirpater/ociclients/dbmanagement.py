import logging
import oci
from ociextirpater.OCIClient import OCIClient

class dbmanagement( OCIClient ):
    service_name = "DB Management"
    clientClass = oci.database_management.DbManagementClient

    objects = [
        {
            "name_singular"      : "Private Endpoint",
            "name_plural"        : "Private Endpoints",
            "function_list"      : "list_db_management_private_endpoints",
            "formatter"          : lambda e: "Private endpoint with OCID {} / name '{}' is in state {}".format(e.id, e.name, e.lifecycle_state),
            "function_delete"    : "delete_db_management_private_endpoint",
        },

        {
            "name_singular"      : "Managed database group",
            "name_plural"        : "Managed database groups",
            "function_list"      : "list_managed_database_groups",
            "formatter"          : lambda g: "Managed db group with OCID {} / name '{}' is in state {}".format(g.id, g.name, g.lifecycle_state),

            "function_delete"    : "delete_managed_database_group",
        },

        {
            "name_singular"      : "External DB system",
            "name_plural"        : "External DB systems",
            "function_list"      : "list_external_db_systems",
            "function_delete"    : "delete_external_db_system",
        },

        {
            "name_singular"      : "External exadata infra",
            "name_plural"        : "External exadata infra",
            "function_list"      : "list_external_exadata_infrastructures",
            "function_delete"    : "delete_external_exadata_infrastructure",
        },

        {
            "name_singular"      : "External mySQL database",
            "name_plural"        : "External mySQL databases",
            "function_list"      : "list_external_my_sql_databases",
            "function_delete"    : "delete_external_my_sql_database",
        },



        # {
        #     "name_singular"      : "XXX",
        #     "name_plural"        : "XXXXs",
        #     "function_list"      : "list_xxx",
        #     "function_delete"    : "delete_xxx",
        # },

        # list_managed_databases
        # delete_external_db_system_connector

        # list_external_db_system_discoveries
        # delete_external_db_system_discovery

        {
            "name_singular"      : "mySQL database connector",
            "name_plural"        : "mySQL database connectors",
            "function_list"      : "list_my_sql_database_connectors",
            "function_delete"    : "delete_external_my_sql_database_connector",
        },

        {
            "name_singular"      : "named credential",
            "name_plural"        : "named credentials",
            "function_list"      : "list_named_credentials",
            "formatter"          : lambda o: "Named credential with OCID {} / name '{}' is in state {}".format(o.id, o.name, o.lifecycle_state),
            "function_delete"    : "delete_named_credential",
        },

    ]

