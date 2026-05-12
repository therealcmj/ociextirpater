import logging

import oci
from ociextirpater.OCIClient import OCIClient

class nosql( OCIClient ):
    service_name = "No SQL"
    clientClass = oci.nosql.NosqlClient
    compositeClientClass = oci.nosql.NosqlClientCompositeOperations

    objects = [
        {
            "name_singular"    : "No SQL table",
            "name_plural"      : "No SQL tables",
            "function_list"    : "list_tables",
            "formatter"        : lambda table: "NOSQL Table with OCID {} / name '{}' is in state {}".format(table.id, table.name, table.lifecycle_state),
            "function_delete"  : "delete_table",

        }
    ]


    def predelete(self,object,region,found_object):
        if object["name_plural"] == "No SQL tables":
            # table will be oci.nosql.models.TableCollection
            from oci.nosql.models.table_collection import TableCollection

            if found_object.is_multi_region:
                # look for replicas and then delete them if they exist
                logging.info("Table {} is multi-region. Determining replicas to delete".format(found_object.id))

                # listing tables doesn't get the replicas so you need to explicitly GET the table again

                f=getattr((self.clients[region]), "get_table")
                table = f( found_object.id ).data
                logging.debug("Table {} retrieved, has {} replicas".format(found_object.id, len(table.replicas)))

                f = getattr((self.compositeClients[region]), "delete_replica_and_wait_for_state")

                for replica in table.replicas:
                    logging.info("Deleting replica in region {} for table {} with OCID {}".format(replica.region, found_object.id, replica.table_id))
                    f( 
                        found_object.id, 
                        replica.region,
                        wait_for_states=[
                            oci.nosql.models.WorkRequest.STATUS_SUCCEEDED,
                            oci.nosql.models.WorkRequest.STATUS_FAILED,
                            oci.nosql.models.WorkRequest.STATUS_CANCELED
                            ]
                    )
                logging.info("Finished deleting replicas for table {}".format(found_object.id))
                return

        raise NotImplementedError
