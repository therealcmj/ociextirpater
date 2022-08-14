import logging

class OCIClient:
    config = None

    clientClass = None
    clients = {}
    isRegional = True

    def _init_regional_client(self,ociconfig,region):
        logging.debug("Initializing {} client for region {}".format(self.clientClass.__name__, region))
        rconfig = ociconfig
        logging.debug("Old region in this OCI config dict: {}".format(rconfig["region"]))
        rconfig["region"] = region
        logging.debug("New region in this OCI config dict: {}".format(rconfig["region"]))
        self.clients[region] = self.clientClass(rconfig)

    def __init__(self,config):
        logging.debug("OCIClient")
        self.config = config

        # if the service IS a regional service then we need one client for each region
        if self.isRegional:
            logging.debug( "Initializing regional OCI clients for {}".format( self.clientClass.__name__))
            for region in self.config.regions:
                self._init_regional_client( config.ociconfig, region)

        # otherwise we only need the one for the Home region
        else:
            logging.debug( "Initializing OCI client in the home region for {}".format( self.clientClass.__name__))
            self._init_regional_client(config.ociconfig, config.home_region)

        logging.debug("{} {} clients initialized".format( len(self.clients), self.clientClass.__name__))

    # I'm not sure if I want to take an argument or not
    def findAndDeleteAllInCompartment(self, compartment):
        raise NotImplementedError()
