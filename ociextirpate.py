#!/usr/bin/env python3

import io
import importlib
import logging

from fdk import response

__requires__ = 'oci==2.78.0'

def extirpate():

    logging.basicConfig(format='%(asctime)s %(threadName)s %(levelname)7s %(module)s:%(funcName)s -> %(message)s', level=logging.INFO)
    logging.info("Starting up")

    logging.info("Configuring...")
    from ociextirpater.config import config
    cfg = config()
    logging.info("Configured")

    # at this point we should have a signer and some other stuff in the cfg object

    clients = cfg.categories_to_delete

    logging.info("{} clients".format( len(clients)))

    for client in clients:
        logging.debug( "Importing {}".format(client))
        my_module = importlib.import_module("ociextirpater.ociclients.%s" % client)
        logging.debug( "Module name: {}".format( my_module.__name__ ))

        logging.debug( "Getting {}".format( client ) )
        cls = getattr( importlib.import_module("ociextirpater.ociclients.%s" % client), client )
        logging.debug( "Name for {} is {}".format( client, cls.service_name ) )

        logging.debug( "Instantiating" )
        o = cls( cfg )
        logging.debug("Instantiated OK")

        # executor.submit(o.findAndDeleteAllInCompartment)
        try:
            o.findAndDeleteAllInCompartment()
        except Exception as e:
            logging.error("Exception caught")
            logging.debug(e)


def handler(ctx, data: io.BytesIO = None):

    extirpate()

    return response.Response(
        ctx, response_data='Finished extirpating',
        headers={"Content-Type": "text/plain"}
    )


if __name__ == '__main__':
    extirpate()