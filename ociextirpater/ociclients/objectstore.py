import logging
import concurrent

import oci
from ociextirpater.OCIClient import OCIClient

class objectstore( OCIClient ):
    service_name = "Object Storage"
    clientClass = oci.object_storage.ObjectStorageClient

    namespace = None

    objects = [
        {
            "name_singular"    : "Private Endpoint",
            "name_plural"      : "Private Endpoints",
            "function_list"    : "list_private_endpoints",
            "function_delete"  : "delete_private_endpoint",
        },

        {
            "name_singular"    : "Object Store bucket",
            "name_plural"      : "Object Store buckets",
            "formatter"        : lambda bucket: "Bucket with name '{}'".format(bucket.name),
            "function_list"    : "list_buckets",
            # Why *did* I have this?
            # Buckets don't have a lifecycle state. And originally I didn't have hasattr() to check
            # for that attribute. So this lambda function was here to avoid an exception being thrown.
            # Once I added hasattr() to check for lifecycle state on the object this become unnecessary.
            # "check2delete"     : lambda bucket: True,
            "children"         : [
                                    {
                                        "function_list"  : "list_replication_policies",
                                        "function_delete": "delete_replication_policy",
                                        "name_singular"  : "Object Replication policy",
                                        "name_plural"    : "Object Replication policies",
                                    },
                                    {
                                        "function_list"  : "list_retention_rules",
                                        "function_delete": "delete_retention_rule",
                                        "name_singular"  : "Object Store Retention rule",
                                        "name_plural"    : "Object Store Retention rules",
                                    },
                                    {
                                        "function_list"  : "list_preauthenticated_requests",
                                        "function_delete": "delete_preauthenticated_request",
                                        "name_singular"  : "Object Store Pre-authenticated request",
                                        "name_plural"    : "Object Store Pre-authenticated requests",
                                    },

                                    {
                                        "function_list"  : "list_multipart_uploads",
                                        "function_delete": "abort_multipart_upload",
                                        "name_singular"  : "Object Store multi-part upload",
                                        "name_plural"    : "Object Store multi-part uploads",
                                    },
                                    {
                                        "function_list"  : "list_objects",
                                        "function_delete": "delete_object",
                                        "name_singular"  : "Object",
                                        "name_plural"    : "Objects",
                                    },
                                    {
                                        "function_list"  : "list_object_versions",
                                        "function_delete": "delete_object",
                                        "name_singular"  : "Object Version",
                                        "name_plural"    : "Object Versions",
                                    },

            ]

        }
    ]

    def __init__(self,config):
        super().__init__(config)

        # we need the namespace
        self.namespace = self.clients[ config.home_region ].get_namespace().data
        logging.debug("Object Store namespace is {}".format(self.namespace))


    def list_objects(self, o, region, this_compartment, **kwargs):
        if o["name_plural"] == "Object Store buckets" or o["name_plural"] == "Private Endpoints":
            logging.debug("Calling oci.pagination.list_call_get_all_results( {}()...".format(o["function_list"]))

            return oci.pagination.list_call_get_all_results(getattr((self.clients[region]), o["function_list"]),
                                                            self.namespace,
                                                            this_compartment,
                                                            **kwargs).data

        # # TODO: combine these
        # if o["name_plural"] == "Object Store buckets":
        #     return oci.pagination.list_call_get_all_results(    getattr((self.clients[region]), "list_buckets"),
        #                                                         self.namespace,
        #                                                         this_compartment,
        #                                                         **kwargs).data
        # if o["name_plural"] == "Private Endpoints":
        #     return oci.pagination.list_call_get_all_results(    getattr((self.clients[region]), "list_private_endpoints"),
        #                                                         self.namespace,
        #                                                         this_compartment,
        #                                                         **kwargs).data

        raise NotImplementedError

    def delete_object(self, oci_object, region, object):
        f = None
        if oci_object["name_singular"] == "Object Store bucket":
            # child objects:
            for child in oci_object["children"]:
                logging.debug( "Listing {} in bucket {}".format( child["name_plural"], object.name ))
                kwargs = {}
                if hasattr( child, "kwargs_list"):
                    kwargs = child["kwargs_list"]
                logging.debug("Getting a list of all {} objects in bucket".format(child["name_singular"]))
                xs = oci.pagination.list_call_get_all_results(  getattr((self.clients[region]), child["function_list"]),
                                                                self.namespace,
                                                                object.name,
                                                                **kwargs).data

                # then we need to delete them
                df = getattr((self.clients[region]), child["function_delete"])
                if child["name_plural"] == "Objects":
                    # then we need to do something special
                    logging.info("Deleting objects in bucket")

                    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                        for obj in xs.objects:
                            logging.debug("Deleting {}".format(obj.name))

                            future = executor.submit(df, self.namespace, object.name, obj.name)

                else:
                    for x in xs:
                        if child["name_singular"] == "Object Store multi-part upload":
                            df(x.namespace, x.bucket, x.object,x.upload_id)
                        elif child["name_singular"] == "Object Store Retention rule":
                            logging.debug("Retention rule is a special case - trying to delete but it may fail")
                            try:
                                df(self.namespace, object.name, x.id )
                            except:
                                logging.debug("delete failed, but continuing...")
                        elif child["name_plural"] == "Object Versions":
                            logging.info("Deleting object versions...ß")
                            # for x in xs:
                            #     logging.debug("Deleting {} version {}".format( x.name, x.version_id ))
                            #     df( object.namespace, object.name, x.name, **{"version_id": x.version_id} )
                            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                                for x in xs:
                                    logging.debug("Deleting {} version {}".format( x.name, x.version_id ))
                                    future = executor.submit(df, object.namespace, object.name, x.name, **{"version_id": x.version_id} )

                            logging.debug("Done deleting object versions")
                        else:
                            df( self.namespace, object.name, x.id )

            logging.debug("Deleting object lifecycle policy")
            f = getattr((self.clients[region]), "delete_object_lifecycle_policy")
            f( self.namespace, object.name )

            f = getattr((self.clients[region]), "delete_bucket")
            logging.debug("calling delete method")
            f(self.namespace, object.name)
        elif oci_object["name_singular"] == "Private Endpoint":
            f = getattr((self.clients[region]), "delete_private_endpoint")
            logging.debug("calling delete method")
            f(self.namespace, object.name)
        else:
            raise NotImplementedError
