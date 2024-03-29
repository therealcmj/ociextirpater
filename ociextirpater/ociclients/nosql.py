import oci
from ociextirpater.OCIClient import OCIClient

class nosql( OCIClient ):
    service_name = "No SQL"
    clientClass = oci.nosql.NosqlClient

    objects = [
        {
            "function_list"    : "list_tables",
            "function_delete"  : "delete_table",
            "name_singular"    : "No SQL table",
            "name_plural"      : "No SQL tables",
        }
    ]
