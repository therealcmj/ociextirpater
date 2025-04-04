import logging
import oci
import time
from ociextirpater.OCIClient import OCIClient

class secrets( OCIClient ):
    service_name = "Vault Secrets"
    clientClass = oci.vault.VaultsClient

    objects = [
        {
            "name_singular"      : "Secret",
            "name_plural"        : "Secrets",
            "formatter"          : lambda secret: "Secret with OCID {} / name '{}' is in state {}".format(secret.id, secret.secret_name, secret.lifecycle_state),

            "function_list"      : "list_secrets",
        },
    ]

    def __init__(self,config):
        logging.warning("Vault secrets cannot be deleted immediately. To allow for compartment deletion secrets will be moved to the specified junkyard compartment and a deletion will be scheduled for 8 days from now...")
        super().__init__(config)

        # save junkyard from the config
        self.junkyard = config.junkyard

    def predelete(self,object,region,found_object):
        if self.junkyard:
            logging.debug("Junkyard is configured")

        if found_object.compartment_id == self.junkyard:
            logging.debug("Secret is already in junkyard compartment and will not be moved")
            return

        if object["name_plural"] == "Secrets":
            logging.debug("Moving secret to junkyard")

            f = getattr((self.clients[region]), "change_secret_compartment")
            f(found_object.id, oci.vault.models.ChangeSecretCompartmentDetails(**{"compartment_id": self.junkyard}))

            # wait to see if it's been moved - 15 seconds seems fair
            wait = 15
            f = getattr((self.clients[region]), "get_secret")
            while wait > 0:
                r = f(found_object.id).data
                if r.compartment_id != self.junkyard or r.lifecycle_state != "ACTIVE":
                    logging.debug("Secret not moved yet. Waiting a second.")
                    time.sleep(1)
                    wait -= 1
                else:
                    logging.info("Secret successfully moved to junkyard")
                    wait = 0

    def delete_object(self, object, region, found_object):
        if object["name_plural"] == "Secrets":
            f = getattr((self.clients[region]), "schedule_secret_deletion")

            from datetime import datetime, timedelta
            nextweek = (datetime.now() + timedelta(days=8)).isoformat() + "+00:00"
            logging.info( "Scheduling deletion of {} for {}".format(object["name_singular"], nextweek ) )

            f( found_object.id, oci.key_management.models.ScheduleVaultDeletionDetails(**{ "time_of_deletion": nextweek} ) )
            return

        raise NotImplementedError

