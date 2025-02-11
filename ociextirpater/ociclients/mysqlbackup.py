import logging
import oci
from ociextirpater.OCIClient import OCIClient

class mysqlbackup( OCIClient ):
    service_name = "MySQL Backup"
    clientClass = oci.mysql.DbBackupsClient

    objects = [
        {
            "name_singular"      : "MySQL Backup",
            "name_plural"        : "MySQL Backups",
            "function_list"      : "list_backups",
            "function_delete"    : "delete_backup",
        },
    ]


