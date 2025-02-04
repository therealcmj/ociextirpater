import logging
import oci
from ociextirpater.OCIClient import OCIClient

class functions( OCIClient ):
    service_name = "Functions"
    clientClass = oci.functions.FunctionsManagementClient

    objects = [
        {
            "name_singular"    : "Functions Application",
            "name_plural"      : "Functions Applications",
            "function_list"    : "list_applications",
            "function_delete"  : "delete_application",
        }
    ]


    def predelete(self,object,region,found_object):
        if object["name_plural"] == "Functions Applications":
            # you cannot delete a Functions Application until you delete all the Functions in it
            fList   = getattr((self.clients[region]), "list_functions")
            fDelete = getattr((self.clients[region]), "delete_function")

            logging.info("Getting all Functions in Application {}".format( found_object.id ))
            # f( found_object.id, { "something": True } )

            fns = oci.pagination.list_call_get_all_results(fList,found_object.id).data
            logging.debug("Found {} Functions in Function App {}".format( len ( fns ), found_object.id))
            for fn in fns:
                logging.debug("Deleting Function {}".format( fn.id) )
                fDelete( fn.id )
            return

        raise NotImplementedError
