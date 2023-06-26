
class config:

    compartment = None
    all_compartments = []
    signer = None
    ociconfig = None
    threads = 1

    home_region = None
    regions = []

    identity_client = None

    # we work through these sequentially in the order specified
    # that doesn't make much of a difference until you get to things like networking
    categories_to_delete =  [
                                "adm",
                                "analytics",
                                "anomaly",
                                "apigateway",
                                "bastion",
                                "datasafe",
                                # "dbtools",
                                "database",
                                "dns",
                                "functions",
                                "nosql",
                                "objectstore",
                                "osms",
                                "vision",
                                "loadbalancers",
                                "certificates",
                                "compute",
                                "computepool",
                                "oke",
                                "network",
                            ]


    def __init__(self):
        import logging, logging.handlers
        import argparse

        # parser = argparse.ArgumentParser(formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=80, width=130))
        parser = argparse.ArgumentParser()

        # I'm going to use most of the same arguments as OCI SuperDelete
        parser.add_argument('-cf', default="~/.oci/config", dest='config_file', help='OCI Config file')
        parser.add_argument('-cp', default="DEFAULT", dest='config_profile', help='Config Profile inside the config file')
        parser.add_argument('-ip', action='store_true', default=False, dest='is_instance_principal', help='Use Instance Principals for Authentication')
        parser.add_argument('-dt', action='store_true', default=False, dest='is_delegation_token', help='Use Delegation Token for Authentication')
        # parser.add_argument('-log', default="log.txt", dest='log_file', help='output log file')
        parser.add_argument('-log', dest='log_file', help='output log file')
        parser.add_argument('-force', action='store_true', default=False, dest='force', help='force delete without confirmation')
        parser.add_argument('-debug', action='store_true', default=False, dest='debug', help='Enable debug')
        parser.add_argument('-skip_delete_compartment', action='store_true', default=False, dest='skip_delete_compartment', help='Skip Deleting the compartment at the end')
        parser.add_argument("-rg", dest='regions', help="Regions to delete comma separated (defaults to all subscribed regions)")
        parser.add_argument("-c", required=True, dest='compartment', help="top level compartment id to delete")
        parser.add_argument("-o", dest="objects",help="Object catagories to work on. See docs for info")
        parser.add_argument("-t", dest="threads",default="1",help="Number of threads")
        cmd = parser.parse_args()
        # if help:
        #     parser.print_help()
        #     # sys.exit(-1)

        # process the logging arguments first
        rootLogger = logging.getLogger()
        #
        if cmd.log_file:
            rootLogger.addHandler( logging.handlers.WatchedFileHandler(cmd.log_file) )
            logging.info("Logging to log file '{}'".format( cmd.log_file))
        #
        if cmd.debug:
            rootLogger.setLevel("DEBUG")
            logging.debug("Log level set to DEBUG")


        # then process the other arguments
        import oci

        logging.info("Preparing signer")
        # we construct the right signer here
        if cmd.is_instance_principal:
            logging.debug("Authenticating with Instance Principal")
            try:
                signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
                self.ociconfig = {
                    'region': signer.region,
                    'tenancy': signer.tenancy_id
                }

            except Exception:
                errTxt = "Error obtaining instance principals certificate, aborting"
                logging.error(errTxt)
                raise Exception(errTxt)

        elif cmd.is_delegation_token:
            logging.debug("Authenticating with Delegation Token")

            self.ociconfig = oci.config.from_file(cmd.config_file, cmd.config_profile)
            delegation_token_location = self.ociconfig["delegation_token_file"]

            with open(delegation_token_location, 'r') as delegation_token_file:
                delegation_token = delegation_token_file.read().strip()
                # get signer from delegation token
                self.signer = oci.auth.signers.InstancePrincipalsDelegationTokenSigner(delegation_token=delegation_token)

        # otherwise use the config file yada yada
        else:
            try:
                self.ociconfig = oci.config.from_file( cmd.config_file,cmd.config_profile )
                self.signer = oci.signer.Signer.from_config(self.ociconfig)
            except:
                errTxt = "Error obtaining authentication, did you configure config file? aborting"
                logging.error(errTxt)
                raise Exception(errTxt)

        logging.info("Signer prepared")

        # Compartment config
        self.compartment = cmd.compartment
        logging.debug( "Root compartment set to '{}'".format( self.compartment ) )

        # let's get the compartment info and show it
        self.identity_client = oci.identity.IdentityClient(self.ociconfig, signer=self.signer)
        try:
            compartment_name = self.identity_client.get_compartment(self.compartment).data.name
            logging.info(
                "Exterpating resources in compartment '{}' (OCID {})".format(compartment_name, self.compartment))
        except:
            logging.error("Failed to get root compartment")
            raise Exception

        # then get a list of the child compartments
        # I could do this recursively but I like to challenge myself sometimes
        logging.info("Getting child compartments")
        compartments_to_traverse = [ self.compartment ]
        self.all_compartments.append( self.compartment )
        while compartments_to_traverse:
            for c in compartments_to_traverse:
                compartments_to_traverse.remove(c)
                found = oci.pagination.list_call_get_all_results(self.identity_client.list_compartments, c).data
                logging.debug( "Found {} child compartments".format( len(found) ) )
                for x in found:
                    logging.debug("Found compartment {} with lifecycle_state {}".format(x.id,x.lifecycle_state))
                    if x.lifecycle_state == "ACTIVE":
                        compartments_to_traverse.append(x.id)
                        self.all_compartments.append(x.id)
                    else:
                        logging.debug("skipping")

        logging.info("{} compartments will be exterpated".format(len(self.all_compartments)))


        # regions
        requested_regions = None
        if cmd.regions:
            logging.debug("Regions specified on command line")
            # TODO: make sure that the user doesn't request a region that they aren't subscribed to
            # requested_regions = cmd.regions.split(",")
            self.regions = cmd.regions.split(",")
        else:
            logging.debug("Regions not specified on command line.")

        if cmd.objects:
            self.categories_to_delete = cmd.objects.split(",")



        logging.info("Getting subscribed regions...")
        regions = self.identity_client.list_region_subscriptions(self.ociconfig["tenancy"]).data
        for region in regions:
            if region.is_home_region:
                self.home_region = region.region_name

            if not cmd.regions:
                self.regions.append( region.region_name )

        logging.info( "Home region: {}".format( self.home_region ) )
        logging.info( "{} Regions to be exterpated: {}".format( len(self.regions), self.regions ) )
