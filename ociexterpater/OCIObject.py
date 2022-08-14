
import logging

class OCIObject:
    config = None

    clientClass = None
    clients = {}
    isRegionalResource = True

    def __init__(self,config):
        logging.debug("OCIObject")
        self.config = config

        logging.debug( "Initializing OCI clients")
        for region in self.config.regions:
            logging.debug( "Initializing {} client for region {}".format( self.clientClass.__name__, region ) )
            rconfig = self.config.ociconfig
            logging.debug( "Old region in this OCI config dict: {}".format( rconfig["region"] ) )
            rconfig["region"] = region
            logging.debug( "New region in this OCI config dict: {}".format( rconfig["region"] ) )
            self.clients[region] = self.clientClass( rconfig )

        logging.debug("{} {} clients initialized".format( len(self.clients), self.clientClass.__name__))

    def findAll(self, compartment):
        raise NotImplementedError()

    def deleteAll(self):
        raise NotImplementedError()
