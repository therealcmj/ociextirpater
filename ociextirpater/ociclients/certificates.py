import logging

import oci
import time
from ociextirpater.OCIClient import OCIClient

class certificates( OCIClient ):
    service_name = "Certificates"
    clientClass = oci.certificates_management.CertificatesManagementClient

    def __init__(self,config):
        logging.warning("Certificates and Certificate Authorities cannot be deleted immediately. To allow for compartment deletion secrets will be moved to the specified junkyard compartment and a deletion will be scheduled for 8 days from now...")
        super().__init__(config)

        # save junkyard from the config
        self.junkyard = config.junkyard

    def list_objects(self, o, region, this_compartment, **kwargs):
        # can these be collapsed?
        if o["name_plural"] == "Certificates":
            return oci.pagination.list_call_get_all_results(
                getattr((self.clients[region]), "list_certificates"),
                **{
                    "compartment_id": this_compartment,
                    # "lifecycle_state": "ACTIVE"
                }).data
        elif o["name_plural"] == "Certificate Authorities":
            return oci.pagination.list_call_get_all_results(
                getattr((self.clients[region]), "list_certificate_authorities"),
                **{
                    "compartment_id": this_compartment,
                    "lifecycle_state": "ACTIVE"
                }).data
        elif o["name_plural"] == "Certificate Authorities Bundles":
            return oci.pagination.list_call_get_all_results(
                getattr((self.clients[region]), "list_ca_bundles"),
                **{
                    "compartment_id": this_compartment,
                    # "lifecycle_state": "ACTIVE"
                }).data
        else:
            raise NotImplementedError

    def predelete(self,object,region,found_object):
        if self.junkyard:
            logging.debug("Junkyard is configured")

        if found_object.compartment_id == self.junkyard:
            logging.debug("{} is already in junkyard compartment and will not be moved".format(found_object.id))
            return

        logging.debug("Determining whether to move {} to junkyard".format(object["name_singular"]))

        f_get = None
        f_move = None
        move_deets = None

        if object["name_plural"] == "Certificates":
            f_get = getattr((self.clients[region]), "get_certificate")
            f_move = getattr((self.clients[region]), "change_certificate_compartment")
            move_deets = oci.certificates_management.models.ChangeCertificateCompartmentDetails(**{"compartment_id": self.junkyard})


        elif object["name_plural"] == "Certificate Authorities":
            f_get = getattr((self.clients[region]), "get_certificate_authority")
            f_move = getattr((self.clients[region]), "change_certificate_authority_compartment")
            move_deets = oci.certificates_management.models.ChangeCertificateAuthorityCompartmentDetails(**{"compartment_id": self.junkyard})
    
        else:
            logging.debug("{} does not require delay to delete. Will be deleted immediately and not moved to junkyard".format(object["name_plural"]))
            return

        logging.debug("Moving {} to junkyard".format(object["name_singular"]))
        f_move(found_object.id, move_deets)

        # wait to see if it's been moved - 15 seconds seems fair
        wait = 15
        while wait > 0:
            r = f_get(found_object.id).data
            if r.compartment_id != self.junkyard or r.lifecycle_state != "ACTIVE":
                logging.debug("{} not moved yet. Waiting a second.".format(object["name_singular"]))
                time.sleep(1)
                wait -= 1
            else:
                logging.info("{} successfully moved to junkyard".format(object["name_singular"]))
                wait = 0


    def delete_object(self, object, region, found_object):
        from datetime import datetime, timedelta, timezone
        at = datetime.now(timezone.utc) + timedelta(days=7, minutes=15)
        tod = at.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        logging.debug("Time of scheduled deletion: {}".format(tod))

        if object["name_plural"] == "Certificates":
            return (self.clients[region]).schedule_certificate_deletion(
                found_object.id,
                schedule_certificate_deletion_details=oci.certificates_management.models.ScheduleCertificateDeletionDetails(time_of_deletion= tod )
            )
        elif object["name_plural"] == "Certificate Authorities":
            return (self.clients[region]).schedule_certificate_authority_deletion(
                found_object.id,
                schedule_certificate_authority_deletion_details=oci.certificates_management.models.ScheduleCertificateAuthorityDeletionDetails(
                    time_of_deletion=tod
                )
            )

        raise NotImplementedError

    objects = [

        # we should probably find associations and terminate them
        # {
        #     "function_list"      : "list_associations",
        #     "kwargs_list"        : {
        #                            },
        #     "function_delete"    : "delete_xxx",
        #     "name_singular"      : "XXX",
        #     "name_plural"        : "XXXXs",
        # },

        {
            "formatter"          : lambda cert: "Certificate OCID {} / name '{}' is in state {}".format( cert.id, cert.name, cert.lifecycle_state ),
            # "function_list"      : "list_certificates",
            # "kwargs_list"        : {
            #                             "lifecycle_state": "ACTIVE"
            #                        },

            # "function_delete"    : "schedule_certificate_deletion",
            "name_singular"      : "Certificate",
            "name_plural"        : "Certificates",
        },

        {
            "name_singular"      : "Certificate Authority",
            "name_plural"        : "Certificate Authorities",

            "formatter"          : lambda ca: "Certificate Authority OCID {} / name '{}' is in state {}".format( ca.id, ca.name, ca.lifecycle_state ),
            "function_list"      : "list_certificate_authorities",
        },

        {
            "name_singular"      : "Certificate Authority Bundle",
            "name_plural"        : "Certificate Authorities Bundles",

            "function_list"      : "list_ca_bundles",
            "function_delete"    : "delete_ca_bundle"
        },

        # {
        #     # "formatter"          : lambda instance: "XXX instance with OCID {} / name '{}' is in state {}".format( instance.id, instance.name, instance.lifecycle_state ),
        #     "function_list"      : "list_xxx",
        #     "kwargs_list"        : {
        #                            },
        #     "function_delete"    : "delete_xxx",
        #     "name_singular"      : "XXX",
        #     "name_plural"        : "XXXXs",
        # },
    ]
