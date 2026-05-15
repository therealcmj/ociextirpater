#!/usr/bin/env python3

from datetime import datetime,timedelta
import io
import importlib
import logging

__requires__ = 'oci>=2.144.0'


### NASTY
### https://stackoverflow.com/questions/18466079/change-the-connection-pool-size-for-pythons-requests-module-when-in-threading
###
### sorry, not sorry
def patch_http_connection_pool(**constructor_kwargs):
    """
    This allows to override the default parameters of the
    HTTPConnectionPool constructor.
    For example, to increase the poolsize to fix problems
    with "HttpConnectionPool is full, discarding connection"
    call this function with maxsize=16 (or whatever size
    you want to give to the connection pool)
    """

    # from oci._vendor.urllib3 import connectionpool, poolmanager
    from urllib3 import connectionpool, poolmanager
    class MyHTTPConnectionPool(connectionpool.HTTPConnectionPool):
        def __init__(self, *args,**kwargs):
            kwargs.update(constructor_kwargs)
            super(MyHTTPConnectionPool, self).__init__(*args,**kwargs)
    poolmanager.pool_classes_by_scheme['http'] = MyHTTPConnectionPool
    # poolmanager.pool_classes_by_scheme['https'] = MyHTTPConnectionPool

try:
    patch_http_connection_pool(maxsize=1000)
except Exception as e:
    logging.warning("Unable to patch HTTPConnectionPool.")
    logging.warning(e)
    logging.info("Continuing with default HTTPConnectionPool settings.")

def extirpate():

    logging.basicConfig(format='%(asctime)s %(threadName)s %(levelname)7s %(module)s:%(funcName)s -> %(message)s')
    logging.getLogger().setLevel(logging.INFO)
    logging.info("Starting up")

    logging.info("Configuring...")
    from ociextirpater.config import config
    cfg = config()
    logging.info("Configured")

    # at this point we should have a signer and some other stuff in the cfg object

    clients = cfg.categories_to_delete

    logging.info("{} clients".format( len(clients)))

    for client in clients:
        try:
            logging.debug( "Importing {}".format(client))
            my_module = importlib.import_module("ociextirpater.ociclients.%s" % client)
            logging.debug( "Module name: {}".format( my_module.__name__ ))

            logging.debug( "Getting {}".format( client ) )
            cls = getattr( importlib.import_module("ociextirpater.ociclients.%s" % client), client )
            logging.debug( "Name for {} is {}".format( client, cls.service_name ) )

            logging.debug( "Instantiating" )
            o = cls( cfg )
            logging.debug("Instantiated OK")

            o.findAndDeleteAllInCompartment()
        except Exception as e:
            logging.error("Exception caught")
            logging.error(e)


def handler(ctx, data: io.BytesIO = None):

    extirpate()
    from fdk import response

    return response.Response(
        ctx, response_data='Finished extirpating',
        headers={"Content-Type": "text/plain"}
    )


if __name__ == '__main__':
    startTime = datetime.now()
    extirpate()
    endTime = datetime.now()
    logging.info("Extirpate started at {}".format( startTime ))
    logging.info("Extirpate ended   at {}".format( endTime ))
    timedelta_total_seconds = (endTime - startTime).total_seconds()
    logging.info("Total time spent (total_seconds): {} seconds".format( timedelta_total_seconds ))
    logging.info("Total time spent: {}".format( endTime - startTime ))
