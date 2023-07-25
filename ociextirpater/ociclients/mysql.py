import oci
from ociextirpater.OCIClient import OCIClient

class mysql( OCIClient ):
    service_name = "MySQL"
    clientClass = oci.mysql.DbSystemClient

    objects = [
        {
            "name_singular"      : "MySQL DB System",
            "name_plural"        : "MySQL DB Systems",

            "function_list"      : "list_db_systems",
        #     "formatter"          : lambda instance: "XXX instance with OCID {} / name '{}' is in state {}".format( instance.id, instance.name, instance.lifecycle_state ),
            "function_delete"    : "delete_db_system",
        },
    ]
