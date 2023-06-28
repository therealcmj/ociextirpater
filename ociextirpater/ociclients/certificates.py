import logging

import oci
from ociextirpater.OCIClient import OCIClient

class certificates( OCIClient ):
    service_name = "Certificates"
    clientClass = oci.certificates_management.CertificatesManagementClient

    def list_objects(self, o, region, this_compartment, **kwargs):
        if o["name_plural"] == "Certificates":
            return oci.pagination.list_call_get_all_results(
                getattr((self.clients[region]), "list_certificates"),
                **{
                    "compartment_id": this_compartment,
                    "lifecycle_state": "ACTIVE"
                }).data
        elif o["name_plural"] == "Certificate Authorities":
            return oci.pagination.list_call_get_all_results(
                getattr((self.clients[region]), "list_certificate_authorities"),
                **{
                    "compartment_id": this_compartment,
                    "lifecycle_state": "ACTIVE"
                }).data
        else:
            raise NotImplementedError

    def delete_object(self, object, region, found_object):
        from datetime import datetime, timedelta
        at = datetime.now() + timedelta(days=7, minutes=5)
        # _details['timeOfDeletion'] = at.isoformat() + "Z"
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
            "function_list": "list_certificate_authorities",
            # "function_delete": "schedule_certificate_authority_deletion",
            "name_singular": "Certificate Authority",
            "name_plural": "Certificate Authorities",
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
