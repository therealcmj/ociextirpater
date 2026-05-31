import logging
import oci
from ociextirpater.OCIClient import OCIClient

class maildelivery( OCIClient ):
    service_name = "Mail Delivery"
    clientClass = oci.email.EmailClient
    compositeClientClass = oci.email.EmailClientCompositeOperations

    objects = [
        {
            "name_singular"      : "Email Domain",
            "name_plural"        : "Email Domains",
            "function_list"      : "list_email_domains",
            "formatter"          : lambda o: "Email domain with OCID {} / name '{}' is in state {}".format(
                                                                                                            o.id, 
                                                                                                            o.name, 
                                                                                                            o.lifecycle_state
                                                                                                            ),
            "function_delete"    : "delete_email_domain",
        },

        {
            "name_singular"      : "Sender",
            "name_plural"        : "Senders",
            "function_list"      : "list_senders",
            "kwargs_list"        :  {
                                        "lifecycle_state": "ACTIVE"
                                    },
            "formatter"          : lambda sender: "Email Sender with OCID {} / address '{}' is in state {}".format(
                                                                                                            sender.id,
                                                                                                            sender.email_address,
                                                                                                            sender.lifecycle_state
                                                                                                            ),

            "function_delete"    : "delete_sender",
        },

        {
            "name_singular"      : "Email IP Pool",
            "name_plural"        : "Email IP Pools",
            "function_list"      : "list_email_ip_pools",
            "function_delete"    : "delete_email_ip_pool",
        },

        {
            "name_singular"      : "Email Return Path",
            "name_plural"        : "Email Return Paths",
            "function_list"      : "list_email_return_paths",
            "function_delete"    : "delete_email_return_path",
        }

        # suppressions are in the root compartment (ocid1.tenancy.xxxx)
        # {
        #     "name_singular"      : "Suppression",
        #     "name_plural"        : "Suppressions",
        #     "function_list"      : "list_suppressions",
        #     "function_delete"    : "delete_suppression",
        # },

    ]

    def findAllInCompartment(self, region, o, this_compartment, **kwargs):
        if o["name_plural"] == "Email Return Paths":
            return self.clients[region].list_email_return_paths( compartment_id=this_compartment ).data.items
            
        return super().findAllInCompartment(region, o, this_compartment, **kwargs)

    def delete_object(self, object, region, found_object):
        if object["name_plural"] == "Email Domains":
            fList = getattr((self.clients[region]), "list_dkims")
            logging.info("Listing DKIMs in domain {}".format(found_object.name))
            dkims = fList( found_object.id ).data.items

            # we need to wait for all DKIMs to be successfully deleted before we try to delete the domain...
            fDelete = getattr((self.compositeClients[region]), "delete_dkim_and_wait_for_state")
            for dkim in dkims:
                if dkim.lifecycle_state in ["CREATING","FAILED","ACTIVE","INACTIVE","NEEDS_ATTENTION", "UPDATING"]:
                    logging.info("Deleting DKIM {}".format(dkim.id))
                    fDelete(dkim.id,[oci.email.models.WorkRequest.STATUS_SUCCEEDED])
                else:
                    logging.info("DKIM {} is in lifecycle state {} - ignoring".format(dkim.id,dkim.lifecycle_state))

            logging.info("DKIM records for domain {} deleted".format(dkim.id))
        
        return super().delete_object(object, region, found_object)
