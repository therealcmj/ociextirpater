import logging

import oci
from ociextirpater.OCIClient import OCIClient

class identity( OCIClient ):
    service_name = "Identity"
    clientClass = oci.identity.IdentityClient
    compositeClientClass = oci.identity.IdentityClientCompositeOperations

    isRegional = False

    objects = [
        {
            "name_singular"      : "Policy",
            "name_plural"        : "Policies",

            "function_list"      : "list_policies",
            "function_delete"    : "delete_policy",
            "formatter"          : lambda policy: "Policy with OCID {} / name '{}' is in state {}".format(policy.id,policy.name,policy.lifecycle_state),
        },

        {
            "name_singular"      : "Tag Namespace",
            "name_plural"        : "Tag Namespaces",

            "function_list"      : "list_tag_namespaces",
            "formatter"          : lambda tagnamespace: "tag Namespaces with OCID {} / name '{}' is in state {}".format(tagnamespace.id, tagnamespace.name, tagnamespace.lifecycle_state),
            "function_delete"    : "cascade_delete_tag_namespace",
        },

        {
            "name_singular"      : "Tag Default",
            "name_plural"        : "Tag Defaults",
            # "check2delete"       : lambda image: hasattr(image, "compartment_id") and image.compartment_id != None,

            # "formatter"          : lambda instance: "XXX instance with OCID {} / name '{}' is in state {}".format( instance.id, instance.name, instance.lifecycle_state ),
            "function_delete"    : "delete_xxx",
        },

    ]

    def predelete(self,object,region,found_object):
        if object["name_plural"] == "Tag Namespaces":
            f = getattr((self.clients[region]), "update_tag_namespace")
            logging.info("Retiring namespace")
            f( found_object.id, { "isRetired": True } )
            return

        raise NotImplementedError

    def list_objects(self, o, region, this_compartment, **kwargs):
        if o["name_plural"] == "Tag Defaults":
            ret = []
            logging.debug("Getting all Tag Defaults in compartment {}".format(this_compartment))
            tds = oci.pagination.list_call_get_all_results( getattr((self.clients[region]), "list_tag_defaults"), **{ "compartment_id": this_compartment}).data
            if len(tds):
                logging.debug("Found {} tag defaults".format( len(tds) ))
                for td in tds:
                    ret.append( td.id )
            return ret

        raise NotImplementedError
