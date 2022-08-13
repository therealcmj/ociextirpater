import logging

import oci
from ociexterpater.OCIObject import OCIObject

class datasafeuserassessment( OCIObject ):
    singularname = "Data Safe User Assesment"
    pluralname = "Data Safe User Assesments"
    clientClass = oci.data_safe.DataSafeClient

    to_delete = []

    def __init__(self, config):
        super(datasafeuserassessment, self).__init__(config)
        logging.debug( "in __init__" )

    def findAll(self, region, compartment):
        uas = oci.pagination.list_call_get_all_results( self.clients[region].list_user_assessments, compartment, compartment_id_in_subtree=True, access_level="ACCESSIBLE").data
        logging.debug( "Found {} {}".format( len( uas ), self.pluralname ))

        # we need to filter out any that are in state DELETED
        for ua in uas:

            logging.debug( "{} with OCID {} / name '{}' is in state {}".format( self.singularname, ua.id, ua.display_name, ua.lifecycle_state ) )
            if ua.lifecycle_state == "DELETED":
                logging.debug( "skipping")
            else:
                logging.debug("Adding {} to delete list".format( ua.id ))
                logging.debug(ua)
                self.to_delete.append( {
                    "id": ua.id,
                    "region": region,
                    "ua": ua
                })

        # logging.debug( "{} {} to be deleted in region {}".format( len( self.to_delete ), self.pluralname, region ) )

    def deleteAll(self):
        logging.debug( "Deleting {} {}".format( len(self.to_delete),self.pluralname))
        for ua in self.to_delete:
            logging.debug("Deleting {} in region {}".format(ua["id"],ua["region"]))
            try:
                self.clients[ua["region"]].delete_user_assessment( ua["id"])
                self.to_delete.remove( ua )
            except:
                logging.error( "Failed to delete {}".format( ua["id"]))
                logging.debug(ua["ua"])
