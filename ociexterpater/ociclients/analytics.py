import logging
import time

import oci
from ociexterpater.OCIClient import OCIClient

class analytics( OCIClient ):
    service_name = "Analytics"
    clientClass = oci.analytics.AnalyticsClient

    objects = [
        {
            "formatter"          : lambda instance: "Analytics instance with OCID {} / name '{}' is in state {}".format( instance.id, instance.name, instance.lifecycle_state ),
            "function_list"      : "list_analytics_instances",
            "function_delete"    : "delete_analytics_instance",
            "name_singular"      : "Analytics instance",
            "name_plural"        : "Analytics instances",
        },
    ]

    def predelete(self,object,region,found_object):
        # we have pre-delete work to do in case d a route table
        if object["name_singular"] == "Analytics instance":
            if found_object.lifecycle_state == found_object.LIFECYCLE_STATE_INACTIVE:
                logging.debug("Instance already stopped")
                return

            logging.info("Stopping {} ".format( object["name_singular"]))
            f = getattr((self.clients[region]), "stop_analytics_instance")
            f( found_object.id, **{})

            f = getattr((self.clients[region]), "get_analytics_instance")
            wait = 300
            # then wait for it to stop
            while wait:
                logging.info("Waiting for instance to stop")
                lifecycle_state = (f( found_object.id ).data).lifecycle_state
                logging.debug("Current lifecycle state is {}".format( lifecycle_state ))


                if lifecycle_state == found_object.LIFECYCLE_STATE_INACTIVE:
                    logging.info( "Instance is stopped")
                    return

                logging.debug("Sleeping")
                time.sleep(1)
                wait -= 1

            raise Exception("Failed to stop in allowed time")

        pass

