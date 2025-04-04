import logging
import time
import oci
from oci.key_management.models import ChangeKeyCompartmentDetails

from ociextirpater.OCIClient import OCIClient

class kms( OCIClient ):
    service_name = "Key Management"
    clientClass = oci.key_management.KmsVaultClient
    junkyard = None

    objects = [
        {
            "name_singular"      : "KMS Vault",
            "name_plural"        : "KMS Vaults",
            "function_list"      : "list_vaults",
        },
    ]

    def __init__(self,config):
        super().__init__(config)
        # save junkyard from the config
        self.junkyard = config.junkyard

    def predelete(self,object,region,found_object):
        if self.junkyard:
            logging.debug("Junkyard is configured")

            if found_object.compartment_id == self.junkyard:
                logging.debug("Vault is already in junkyard compartment and will not be moved")
                return

            if object["name_plural"] == "KMS Vaults":
                logging.warning("KMS Vaults cannot be deleted immediately. To allow for compartment deletion the vault and its keys will be moved to the specified junkyard compartment and a deletion will be scheduled for 7 days from now...")
                logging.warning("NOTE: this code only finds keys in the same compartment as the vault. Keys located elsewhere in the tenancy will NOT be moved but WILL be scheduled for deletion.")

                kmsc = oci.key_management.kms_management_client.KmsManagementClient(self.config.ociconfig, found_object.management_endpoint)

                logging.info("Listing keys in vault {}".format(found_object.display_name))
                keys = oci.pagination.list_call_get_all_results(kmsc.list_keys,
                                                              found_object.compartment_id,
                                                              **{}).data
                if keys:
                    for key in keys:
                        logging.debug("Moving key {} to junkyard".format(key.id))
                        kmsc.change_key_compartment(key.id, ChangeKeyCompartmentDetails(**{"compartment_id":self.junkyard}))
                else:
                    logging.debug("No keys found in same compartment as vault {}".format(found_object.display_name))

                return

        raise NotImplementedError


    def delete_object(self, object, region, found_object):
        if object["name_plural"] == "KMS Vaults":
            if self.junkyard:
                if found_object.compartment_id == self.junkyard:
                    logging("Vault is already in junkyard.")
                else:
                    logging.debug("Moving vault to junkyard")

                    # problem - there is no composite operation. SD:SDK-6807
                    f = getattr((self.clients[region]), "change_vault_compartment")
                    f(found_object.id,oci.key_management.models.ChangeVaultCompartmentDetails(**{"compartment_id":self.junkyard}))

                    # so we just check to see if it's been moved
                    # 15 seconds seems fair
                    wait = 15
                    f = getattr((self.clients[region]), "get_vault")
                    while wait > 0:
                        r = f(found_object.id).data
                        if r.compartment_id != self.junkyard or r.lifecycle_state != "ACTIVE":
                            logging.debug("Vault not moved yet. Waiting a second.")
                            time.sleep(1)
                            wait -= 1
                        else:
                            logging.info("Vault successfully moved to junkyard")
                            wait = 0

            f = getattr((self.clients[region]), "schedule_vault_deletion")

            from datetime import datetime, timedelta
            nextweek = (datetime.now() + timedelta(days=8)).isoformat() + "+00:00"
            logging.info( "Scheduling deletion of {} for {}".format(object["name_singular"], nextweek ) )

            f( found_object.id, oci.key_management.models.ScheduleVaultDeletionDetails(**{ "time_of_deletion": nextweek} ) )
            return

        raise NotImplementedError
