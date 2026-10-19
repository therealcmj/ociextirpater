import logging
import oci
from ociextirpater.OCIClient import OCIClient


class email(OCIClient):
    service_name = "Email"
    clientClass = oci.email.email_client.EmailClient

    objects = [
        {
            "name_singular"      : "EMail Domain",
            "name_plural"        : "EMail Domains",
            "function_list"      : "list_email_domains",
            "function_delete"    : "delete_email_domain",
        },

        # DKIMs are children of the domain, so we delete them inside there
        # Note: they live in the same compartment as the domain.
        # {
        #     "name_singular"      : "DKIM",
        #     "name_plural"        : "DKIMs",
        #     "function_list"      : "list_dkims",
        #     "function_delete"    : "delete_dkim",
        # },


        {
            "name_singular"      : "EMail IP Pool",
            "name_plural"        : "EMail IP Pools",
            "function_list"      : "list_email_ip_pools",
            "function_delete"    : "delete_email_ip_pool",
        },


        {
            "name_singular"      : "EMail Return Path",
            "name_plural"        : "EMail Return Paths",
            "function_list"      : "list_email_return_paths",
            "function_delete"    : "delete_email_return_path",
        },


        {
            "name_singular"      : "Email Sender",
            "name_plural"        : "Email Senders",
            "function_list"      : "list_senders",
            "function_delete"    : "delete_sender",
        },


        # Suppressions only work at the root of the tenancy
        # {
        #     "name_singular"      : "Suppression",
        #     "name_plural"        : "Suppressions",
        #     "function_list"      : "list_suppressions",
        #     "function_delete"    : "delete_suppression",
        # }
    ]

    # def findAllInCompartment(self, region, o, this_compartment, **kwargs):
    #     import logging
    #     logging.warning("Calling super() to find all {} in compartment".format(o["name_plural"]))
    #     return super().findAllInCompartment(region, o, this_compartment, **kwargs)

    def delete_object(self, object, region, found_object):
        if object["name_plural"] == "EMail Domains":
            logging.info("Checking for DKIMs in domain {} before attempting to delete email domain".format(found_object.id))

            # this is a tricky trick I may regret in the future
            # finfAllInCompartment takes a compartment ID.
            # But I'm going to pass in the domain which goes in the same param
            # order as compartment usually does.
            temp_obj = {
                            "name_singular"      : "DKIM",
                            "name_plural"        : "DKIMs",
                            "function_list"      : "list_dkims",
                            "function_delete"    : "delete_dkim",
                        }

            dkims = self.findAllInCompartment(region, temp_obj, found_object.id)
            for dkim in dkims:
                logging.info("Deleting DKIM {}".format(dkim.id))
                self.delete_object(
                            temp_obj,
                            region,
                            dkim)
                
        return super().delete_object(object, region, found_object)

