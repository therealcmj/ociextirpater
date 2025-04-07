import logging
import oci
from oci.mysql.models import DeletionPolicyDetails

from ociextirpater.OCIClient import OCIClient

class mysql( OCIClient ):
    service_name = "MySQL"
    clientClass = oci.mysql.DbSystemClient

    objects = [
        {
            "name_singular"      : "MySQL DB System",
            "name_plural"        : "MySQL DB Systems",

            "function_list"      : "list_db_systems",
            "function_delete"    : "delete_db_system",
        },
    ]

    def predelete(self,object,region,found_object):
        if object["name_plural"] == "MySQL DB Systems":
            if not found_object.deletion_policy.is_delete_protected:
                logging.debug("{} is not delete protected".format(object["name_singular"]))
                return


            f = getattr((self.clients[region]), "update_db_system")
            logging.info("Updating DB system to remove delete protection")
            # dp = found_object.deletion_policy
            # dp.is_delete_protected = False
            dp = {
                    "automaticBackupRetention": DeletionPolicyDetails.AUTOMATIC_BACKUP_RETENTION_DELETE,
                    "finalBackup": DeletionPolicyDetails.FINAL_BACKUP_SKIP_FINAL_BACKUP,
                    "isDeleteProtected": False
            }
            found_object.deletion_policy.is_delete_protected = False
            f( found_object.id, { "deletionPolicy" : dp } )
            return

        raise NotImplementedError
