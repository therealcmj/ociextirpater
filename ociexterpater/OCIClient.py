import logging
import oci

class OCIClient:
    config = None

    clientClass = None
    clients = {}
    isRegional = True
    searches_are_recursive = True


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

        if not self.searches_are_recursive:
            # in cases where the searches aren't recursive we have to search all of the child compartments too
            # so let's do that first
            for child in self.config.all_compartments:
                logging.debug( "executing findAndDeleteAllInCompartment on child compartment {}".format( child ))
                self.findAndDeleteAllInCompartment( child )

        for object in self.objects:
            logging.debug("Singular name: {}".format(object["name_singular"]))

            for o in self.objects:
                for region in self.clients:
                    # self.clients is a dict from region name to the actual client for that region.
                    logging.info( "Finding all {} in compartment {} in region {}".format( o["name_plural"], compartment, region))
                    kwargs = o["kwargs_list"]
                    os = oci.pagination.list_call_get_all_results(  getattr( (self.clients[region]), o["function_list"] ),
                                                                    compartment,
                                                                    **kwargs).data
                    # compartment_id_in_subtree = True, access_level = "ACCESSIBLE").data
                    logging.info( "Found {} {}".format( len( os ), o["name_plural"] ) )

                    f = getattr((self.clients[region]), o["function_delete"])

                    # we need to filter out any that are in state DELETED
                    for o2 in os:
                        logging.info( "{} with OCID {} / name '{}' is in state {}".format( o["name_singular"], o2.id, o2.display_name, o2.lifecycle_state ) )

                        # TODO:
                        # if the object has a filter_func we need to use that instead of checking if it has a lifecycle state of DELETED or DELETING

                        if o2.lifecycle_state == "DELETED" or o2.lifecycle_state == "DELETING":
                            logging.debug( "skipping")
                        else:
                            logging.info("Deleting {}".format(o2.id))
                            try:
                                f( o2.id )

                            except Exception as e:
                                logging.error( "Failed to delete {} because {}".format(e))
                                logging.debug(e)

