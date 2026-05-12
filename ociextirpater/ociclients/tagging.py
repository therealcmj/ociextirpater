import logging
import oci
from ociextirpater.OCIClient import OCIClient

class tagging( OCIClient ):
    service_name = "Tagging"
    clientClass = oci.identity.identity_client.IdentityClient
    compositeClientClass = oci.identity.identity_client_composite_operations.IdentityClientCompositeOperations
    isRegional = False

    objects = [
        {
            "name_singular"      : "Tag Namespace",
            "name_plural"        : "Tag Namespaces",

            "function_list"      : "list_tag_namespaces",
            "formatter"          : lambda tagnamespace: "tag Namespaces with OCID {} / name '{}' is in state {}".format(tagnamespace.id, tagnamespace.name, tagnamespace.lifecycle_state),
            # "function_delete"    : "cascade_delete_tag_namespace",
            # "c_function_delete"  : "cascade_delete_tag_namespace_and_wait_for_state",
        },
    ]

    def predelete(self,object,region,found_object):
        if object["name_plural"] == "Tag Namespaces":
            logging.info("Namespace is currently in lifecycle state {}".format(found_object.lifecycle_state))
            if found_object.lifecycle_state == "ACTIVE":
                logging.info("Retiring namespace before deletion")

                f = getattr((self.compositeClients[region]), "update_tag_namespace_and_wait_for_state")
                logging.info("Retiring namespace")
                f( found_object.id,
                   { "isRetired": True },
                   wait_for_states=[
                       oci.identity.models.TagNamespace.LIFECYCLE_STATE_INACTIVE
                       ]
                )
            else:
                logging.info("Namespace is already retired. No need to retire before deletion.")
        return

    def delete_object(self, object, region, found_object):
        if object["name_plural"] == "Tag Namespaces":
            f = getattr((self.clients[region]), "cascade_delete_tag_namespace")
            logging.info("Deleting namespace")
            result = f( found_object.id, **{"is_lock_override": True} )

            wrid = result.headers['opc-work-request-id']
            logging.debug("Work request ID for delete operation: {}".format(wrid))

            f = getattr((self.clients[region]), "get_tagging_work_request")
            logging.info("Waiting for namespace to be deleted (work request id {})".format(wrid))
            oci.wait_until(
                self.clients[region],
                f(wrid),
                max_wait_seconds=3600,
                evaluate_response=lambda r: getattr(r.data, 'status') and getattr(r.data, 'status').lower() in ['succeeded']
            )

        raise NotImplementedError
