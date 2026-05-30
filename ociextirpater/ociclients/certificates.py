import logging
import oci
from ociextirpater.OCIClient import OCIClient

class certificates( OCIClient ):
    service_name = "Certificates"
    clientClass = oci.certificates_management.CertificatesManagementClient

    def __init__(self,config):
        logging.warning("Certificates and Certificate Authorities cannot be deleted immediately. To allow for compartment deletion secrets will be moved to the specified junkyard compartment and a deletion will be scheduled for 8 days from now...")
        super().__init__(config)

        # save junkyard from the config
        self.junkyard = config.junkyard

    objects = [

        # Eventually we should probably associations and report them out
        {
            "name_singular"      : "Certificate Association",
            "name_plural"        : "Certificate Associations",
            "function_list"      : "list_associations",
            "check2delete"       : lambda o: False
        },

        {
            "formatter"          : lambda cert: "Certificate OCID {} / name '{}' is in state {}".format( cert.id, cert.name, cert.lifecycle_state ),
            "name_singular"      : "Certificate",
            "name_plural"        : "Certificates",
            "function_list"      : "list_certificates",
            "function_get"       : "delete_certificate",
            "function_move"      : "change_certificate_compartment",

        },

        {
            "name_singular"      : "Certificate Authority",
            "name_plural"        : "Certificate Authorities",

            "formatter"          : lambda ca: "Certificate Authority OCID {} / name '{}' is in state {}".format( ca.id, ca.name, ca.lifecycle_state ),
            "function_list"      : "list_certificate_authorities",
            "function_get"       : "get_certificate_authority",
            "function_move"      : "change_certificate_authority_compartment",
        },

        {
            "name_singular"      : "Certificate Authority Bundle",
            "name_plural"        : "Certificate Authorities Bundles",

            "function_list"      : "list_ca_bundles",
            "function_delete"    : "delete_ca_bundle"
        },

    ]

    def move_to_junkyard(self,object,region,found_object):
        # this will only be called if:
        # 1) a junkyard is configured
        # 2) the object can be moved to a junkyard (i.e. it has a function_move defined)
        # 3) is not already in the junkyard

        # we need the "get" function in order to see that the move has completed successfully
        # if either of these are not defines we'll crash out with an exception - which should be caught above
        
        f_get = getattr((self.clients[region]), object["function_get"])
        f_move = getattr((self.clients[region]), object["function_move"])
        move_deets = None

        if object["name_plural"] == "Certificates":
            move_deets = oci.certificates_management.models.ChangeCertificateCompartmentDetails(**{"compartment_id": self.junkyard})


        elif object["name_plural"] == "Certificate Authorities":
            move_deets = oci.certificates_management.models.ChangeCertificateAuthorityCompartmentDetails(**{"compartment_id": self.junkyard})
    
        else:
            raise Exception("Object {} does not have a configured move to junkyard function".format(object["name_singular"]))

        logging.debug("Moving {} to junkyard".format(object["name_singular"]))
        f_move(found_object.id, move_deets)

        oci.wait_until(
            self.clients[region],
            f_get(found_object.id),
            evaluate_response=lambda r: r.data.lifecycle_state == "ACTIVE" and r.data.compartment_id == self.junkyard,
            max_wait_seconds=60
        )
        logging.debug("{} successfully moved to junkyard".format(object["name_singular"]))


    def delete_object(self, object, region, found_object):
        # TODO: eventually we'll have OCIClient look for and call move_to_junkyard directly instead of having it be the responsibility of each class

        if "function_move" in object and self.junkyard:
            logging.debug("Junkyard is configured and object {} supports moving".format(object["name_singular"]))
        
            if found_object.compartment_id == self.junkyard:
                logging.debug("{} is already in junkyard compartment and will not be moved".format(found_object.id))

            else:
                logging.debug("{} is not in junkyard compartment and will be moved there before deletion".format(found_object.id))
                try:
                    self.move_to_junkyard(object, region, found_object)
                except Exception as e:
                    logging.error("Failed to move {} {} to junkyard. Will attempt deletion anyway. Error was: {}".format(object["name_singular"], found_object.id, e))

        if object["name_plural"] == "Certificates":
            return (self.clients[region]).schedule_certificate_deletion(
                found_object.id,
                schedule_certificate_deletion_details=oci.certificates_management.models.ScheduleCertificateDeletionDetails(
                    time_of_deletion=self.calculate_scheduled_deletion_time(object)
                )
            )
        elif object["name_plural"] == "Certificate Authorities":
            return (self.clients[region]).schedule_certificate_authority_deletion(
                found_object.id,
                schedule_certificate_authority_deletion_details=oci.certificates_management.models.ScheduleCertificateAuthorityDeletionDetails(
                    time_of_deletion=self.calculate_scheduled_deletion_time(object)
                )
            )

        logging.debug( "{} can be deleted immediately".format(object["name_singular"]))
        return super().delete_object(object, region, found_object)

    def calculate_scheduled_deletion_time(self, object):
        logging.debug("Calculating minimum valid scheduled deletion time for {}".format(object["name_singular"]))
        from datetime import datetime, timedelta, timezone
        at = datetime.now(timezone.utc) + timedelta(days=7, minutes=15)
        tod = at.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        logging.debug("Time of scheduled deletion: {}".format(tod))
        return tod


    def findAllInCompartment(self, region, o, this_compartment, **kwargs):
        f = getattr((self.clients[region]), o["function_list"])

        kwargs_list = {}
        # this isn't a thing for anything in the certificates client class.
        # But leaving here as a prototype if things change in the future.
        # if "kwargs_list" in o:
        #     kwargs_list = o.get("kwargs_list", {})
        
        kwargs_list["compartment_id"] = this_compartment
        
        if o["name_plural"] == "Certificate Associations":
            logging.debug("Certificate Associations cannot be deleted directly. We are only reporting them out here for visibility.")
        else:
            kwargs_list["lifecycle_state"] = "ACTIVE"

        return oci.pagination.list_call_get_all_results(
            f,
            **kwargs_list).data
    
            # **{
            #     "compartment_id": this_compartment,
            #     "lifecycle_state": "ACTIVE"
            # }).data
