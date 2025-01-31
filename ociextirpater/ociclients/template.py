import logging
import oci
from ociextirpater.OCIClient import OCIClient

class xxx( OCIClient ):
    service_name = "XXX"
    clientClass = oci.xxx.YYY

    objects = [
        # {
        #     "name_singular"      : "XXX",
        #     "name_plural"        : "XXXXs",
        #     "function_list"      : "list_xxx",
        #     "function_delete"    : "delete_xxx",
        # },

        # {
        #     "name_singular"      : "XXX",
        #     "name_plural"        : "XXXXs",
        #     "check2delete"       : lambda image: hasattr(image, "compartment_id") and image.compartment_id != None,

        #     "function_list"      : "list_xxx",
        #     "kwargs_list"        : {
        #                            },
        #     "formatter"          : lambda instance: "XXX instance with OCID {} / name '{}' is in state {}".format( instance.id, instance.name, instance.lifecycle_state ),
        #     "function_delete"    : "delete_xxx",
        # },
    ]



    # def predelete(self,object,region,found_object):
    #     if object["name_plural"] == "XXX":
    #         f = getattr((self.clients[region]), "update_XXX")
    #         logging.info("info message here")
    #         f( found_object.id, { "something": True } )
    #         return
    #
    #     raise NotImplementedError

    # def delete_object(self, object, region, found_object):
    #     if object["name_plural"] == "DNS Resolver Endpoints":
    #         # DNS Resolver Endpoints
    #         f = getattr((self.clients[region]), "delete_resolver_endpoint")
    #         logging.info( "Deleting {}".format(object["name_singular"]) )
    #         f( found_object["endpoint_id"], found_object["name"] )
    #         return
    #
    #     raise NotImplementedError
