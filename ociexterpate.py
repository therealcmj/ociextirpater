#!/usr/bin/env python3

import importlib
import oci
import logging

__requires__ = 'oci==2.78.0'

if __name__ == "__main__":

    logging.basicConfig(format='%(asctime)s %(levelname)7s %(module)s:%(funcName)s -> %(message)s', level=logging.INFO)
    logging.info("Starting up")

    from ociexterpater.config import config
    cfg = config()

    # at this point we should have a signer and some other stuff in the cfg object

    # let's get the compartment info and show it
    ic = oci.identity.IdentityClient( cfg.ociconfig, signer=cfg.signer)
    try:
        compartment_name = ic.get_compartment(cfg.compartment,retry_strategy=oci.retry.DEFAULT_RETRY_STRATEGY).data.name
        logging.info("Exterpating resources in compartment '{}' (OCID {})".format(compartment_name,cfg.compartment))
    except:
        logging.error("Failed to get compartment")
        raise

    clients = [
        "datasafe"
    ]

    for client in clients:
        logging.debug( "Importing {}".format(client))
        my_module = importlib.import_module("ociexterpater.ociclients.%s" % client)
        logging.debug( "Module name: {}".format( my_module.__name__ ))

        logging.debug( "Getting {}".format( client ) )
        cls = getattr( importlib.import_module("ociexterpater.ociclients.%s" % client), client )
        logging.debug( "Name for {} is {}".format( client, cls.service_name ) )

        logging.debug( "Instantiating" )
        o = cls( cfg )
        logging.debug("OK")

        o.findAndDeleteAllInCompartment(cfg.compartment)


    # # which objects to delete should be a command line argument
    # objs = [
    #     "datasafeuserassessment"
    # ]
    #
    # for obj in objs:
    #     logging.debug( "Importing {}".format(obj))
    #     my_module = importlib.import_module("ociexterpater.ociobjects.%s" % obj)
    #     print( my_module.__name__ )
    #
    #     logging.debug( "Getting {}".format( obj ) )
    #     cls = getattr( importlib.import_module("ociexterpater.ociobjects.%s" % obj), obj )
    #     logging.debug( "Plural name for {} is {}".format( obj, cls.pluralname ) )
    #
    #     logging.debug( "Instantiating" )
    #     o = cls( cfg )
    #     logging.debug("OK")
    #
    #     if o.isRegionalResource:
    #         for region in cfg.regions:
    #             o.findAll( region, cfg.compartment )
    #             o.deleteAll()
    #     else:
    #         o.findAll( config.home_region, cfg.compartment )
    #         o.deleteAll( )

    # # execute a search
    # search = oci.resource_search.ResourceSearchClient(cfg.ociconfig, signer=cfg.signer)
    #
    # sdetails = oci.resource_search.models.StructuredSearchDetails()
    # sdetails.query = 'query all resources where compartmentId = "{}"'.format(cfg.compartment)
    # logging.debug("Executing structured search w/ search string: {}".format( sdetails.query) )
    #
    # try:
    #     result = search.search_resources(search_details=sdetails, limit=1000, retry_strategy=oci.retry.DEFAULT_RETRY_STRATEGY).data
    #
    #     # result.items has everything we found in it
    #
    #     for item in result.items:
    #         logging.info("Found item {} of type {}".format( item.identifier, item.resource_type))
    #         logging.debug( item )
    #
    #         # for each of the items we find we need to proces it
    #
    #     # print(result.items)
    # except oci.exceptions.ServiceError as response:
    #     logging.error("Error searching resources: {} - {}".format(response.code, response.message))
    #     result = oci.resource_search.models.ResourceSummaryCollection()
    #     result.items = []
