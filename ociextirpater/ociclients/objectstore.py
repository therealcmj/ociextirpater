import logging

import oci
from ociextirpater.OCIClient import OCIClient

class objectstore( OCIClient ):
    service_name = "Object Storage"
    clientClass = oci.object_storage.ObjectStorageClient

    namespace = None

    # def list_buckets(self, region, o, this_compartment, **kwargs ):
    #     os = oci.pagination.list_call_get_all_results(getattr((self.clients[region]), "list_buckets"),
    #                                                   self.namespace,
    #                                                   this_compartment,
    #                                                   **kwargs).data

    objects = [
        {
            # "function_list"    : None,
            "kwargs_list"      : {
                                 },
            # this is an example of a lambda function to filter out objects with the field "foo" set to "XXX"
            # "filter_func"      : lambda o: not o["foo"] == "XXX",
            # "function_delete"  : None,
            "name_singular"    : "Object Store bucket",
            "name_plural"      : "Object Store buckets",
            "formatter"        : lambda bucket: "Bucket with name '{}'".format(bucket.name),
            "check2delete"     : lambda bucket: True,
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
                                    }
            ]

        }
    ]

    def __init__(self,config):
        super().__init__(config)

        # we need the namespace
        self.namespace = self.clients[ config.home_region ].get_namespace().data
        logging.debug("Object Store namespace is {}".format(self.namespace))


    def list_objects(self, o, region, this_compartment, **kwargs):
        if o["name_plural"] == "Object Store buckets":
            return oci.pagination.list_call_get_all_results(    getattr((self.clients[region]), "list_buckets"),
                                                                self.namespace,
                                                                this_compartment,
                                                                **kwargs).data
        else:
            raise NotImplementedError

    def delete_object(self, oci_object, region, object):
        f = None
        if oci_object["name_singular"] == "Object Store bucket":
            logging.debug("Deleting object lifecycle policy")
            f = getattr((self.clients[region]), "delete_object_lifecycle_policy")
            f( self.namespace, object.name )

            # child objects:
            for child in oci_object["children"]:
                logging.debug( "Listing {} in bucket {}".format( child["name_plural"], object.name ))
                kwargs = {}
                if hasattr( child, "kwargs_list"):
                    kwargs = child["kwargs_list"]
                logging.debug("Getting a list of all objects in bucket")
                xs = oci.pagination.list_call_get_all_results(  getattr((self.clients[region]), child["function_list"]),
                                                                self.namespace,
                                                                object.name,
                                                                **kwargs).data

                # then we need to delete them
                df = getattr((self.clients[region]), child["function_delete"])
                if child["name_plural"] == "Objects":
                    # then we need to do something special
                    logging.info("Deleting objects in bucket")
                    i = 0
                    for obj in xs.objects:
                        logging.debug("Deleting {}".format(obj.name))
                        df( self.namespace, object.name, obj.name )
                        i = i+1
                        if 0 == i % 100:
                            logging.info("Deleted {} objects from bucket so far".format(i))

                else:
                    for x in xs:
                        if child["name_singular"] == "Object Store multi-part upload":
                            df(self.namespace, object.name, x.id)
                        else:
                            df( self.namespace, object.name, x.id )


            f = getattr((self.clients[region]), "delete_bucket")
            logging.debug("calling delete method")
            f(self.namespace, object.name)
        else:
            raise NotImplementedError
