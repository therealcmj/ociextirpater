import logging
import oci
from ociextirpater.OCIClient import OCIClient

class consoledashboards( OCIClient ):
    service_name = "Console Dashboard"
    clientClass = oci.dashboard_service.DashboardGroupClient

    # technically this is a "home region only" thing but please see note in the DashBoardClient
    # so I'm going to delete them everywhere

    rdcs = {}
    rdccs = {}

    objects = [
        {
            "name_singular"      : "Dashboard Group",
            "name_plural"        : "Dashboard Groups",
            "function_list"      : "list_dashboard_groups",
        },
    ]

    def __init__(self,config):
        for region in config.regions:
            logging.info("Getting ADs for region {}".format(region))
            import oci.dashboard_service.dashboard_client_composite_operations
            rconfig = config.ociconfig
            rconfig["region"] = region
            self.rdcs[region]  = oci.dashboard_service.dashboard_client.DashboardClient( rconfig, signer=config.signer )
            self.rdccs[region] = oci.dashboard_service.dashboard_client_composite_operations.DashboardClientCompositeOperations( self.rdcs[region] )

        super().__init__(config)


    def delete_object(self, object, region, found_object):
        # right now there's only one object - the Dashboard Group.
        # However, you can't just go delete Dashboard Group. First you need to delete the Dashboards in the group

        logging.info("Getting dashboards in dashboard group {}".format( found_object.id))
        dbs = self.rdcs[region].list_dashboards( found_object.id ).data.items

        for db in dbs:
            logging.info("Deleting dashboard with ID {} (from dashboard group {}".format( db.id, found_object.id))
            self.rdccs[region].delete_dashboard_and_wait_for_state( db.id, ["SUCCESS"])

        self.clients[region].delete_dashboard_group( found_object.id )
