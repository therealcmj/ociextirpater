import logging, logging.handlers
import argparse
import os

class config:
    compartments = []
    all_compartments = []
    signer = None
    ociconfig = None
    threads = 1

    class tagCheck:
        _isDefined = False
        _tagNamespace = None
        _tagName = None
        _tagValue = None

        def __init__(self, skiptag):
            # defined tags always have a namespace + dot + name
            self._isDefined = "." in skiptag
            if self._isDefined:
                (self._tagNamespace, self._tagName) = skiptag.split(".")
            else:
                self._tagName = skiptag

            if "=" in self._tagName:
                (self._tagName, self._tagValue) = self._tagName.split("=")
        def isDefined(self):
            return self._isDefined

        def tagNamespace(self):
            return self._tagNamespace
        def tagName(self):
            return self._tagName

        def tagValue(self):
            return self._tagValue

    skiptagged = None

    home_region = None
    regions = []

    identity_client = None

    var_prefix = 'EXTFN'

    # we work through these sequentially in the order specified
    # that doesn't make much of a difference until you get to things like networking
    categories_to_delete =  [
                                "cloudguard",
                                "managementdashboard",
                                "managementagent",
                                "monitoring",
                                "events",
                                "notifications",
                                "osms",
                                "serviceconnector",
                                "loganalytics",
                                "ocilogging",
                                "adm",
                                "analytics",
                                # "aidocument",
                                # "ailanguage",
                                # "aispeech",
                                # "aivision",
                                "apigateway",
                                "bastion",
                                "datasafe",
                                "dbtools",
                                "dbrecovery",
                                "database",
                                "nosql",
                                "mysql",
                                "dns",
                                "functions",
                                "objectstore",
                                "fss",
                                "loadbalancers",
                                "nwloadbalancers",
                                "certificates",
                                "compute",
                                "cache",
                                "computepool",
                                "computemanagement",
                                "oke",
                                "artifacts",
                                "blockstorage",
                                "resourcemanager",
                                "nwfw",
                                "npa",
                                "network",
                                "maildelivery",
                                "healthchecks",
                                "stream",
                                "vss",
                                "waf",
                                "identity",
                                "compartments",
    ]


    def __init__(self):
        args = self.get_args() if not os.getenv(f'{self.var_prefix}_RESOURCE_PRINCIPAL') else self.make_namespace()
        args = self.get_env_vars(args)

        valid = self.validate(args)
        if not valid[0]:
            raise Exception(f'Missing argument {valid[1]}')
        
        self.process(args)
    

    def get_args(self):
        parser = argparse.ArgumentParser()

        # I'm going to use most of the same arguments as OCI SuperDelete
        parser.add_argument('-cf', default="~/.oci/config", dest='config_file', help='OCI Config file')
        parser.add_argument('-cp', default="DEFAULT", dest='config_profile', help='Config Profile inside the config file')
        parser.add_argument('-ip', action='store_true', default=False, dest='is_instance_principal', help='Use Instance Principals for Authentication')
        parser.add_argument('-dt', action='store_true', default=False, dest='is_delegation_token', help='Use Delegation Token for Authentication')
        parser.add_argument('-log', dest='log_file', help='output log file')
        parser.add_argument('-force', action='store_true', default=False, dest='force', help='force delete without confirmation')
        parser.add_argument('-debug', action='store_true', default=False, dest='debug', help='Enable debug')
        parser.add_argument('-skip_tagged', dest='skip_tagged', help='Skip resources tagged specific ways [namespace.]name[=value]')
        parser.add_argument('-skip_delete_compartment', action='store_true', default=False, dest='skip_delete_compartment', help='Skip Deleting the compartment at the end')
        parser.add_argument("-rg", dest='regions', help="Regions to delete comma separated (defaults to all subscribed regions)")
        parser.add_argument("-c", dest='compartment', action="append", help="top level compartment id to delete")
        parser.add_argument("-o", dest="objects",help="Object catagories to work on. See docs for info")
        parser.add_argument("-t", dest="threads",default=-1, type=int, help="Number of threads")
        cmd = parser.parse_args()
        return cmd
    
    def get_env_vars(self, cmd):
        prefix = os.getenv('EXTIRPATER_PREFIX', self.var_prefix)

        # Required
        # The compartment variable needs to be a list derived from a comma separated string
        if os.getenv(f'{prefix}_COMPARTMENT'):
            cmd.compartment = os.getenv(f'{prefix}_COMPARTMENT').split(',')

        cmd.config_file = os.getenv(f'{prefix}_CONFIG_FILE', cmd.config_file)
        cmd.config_profile = os.getenv(f'{prefix}_CONFIG_PROFILE', cmd.config_profile)
        cmd.log_file = os.getenv(f'{prefix}_LOG_FILE', cmd.log_file)
        cmd.regions = os.getenv(f'{prefix}_REGIONS', cmd.regions)
        cmd.objects = os.getenv(f'{prefix}_OBJECTS', cmd.objects)
        cmd.threads = int(os.getenv(f'{prefix}_THREADS', cmd.threads))
        cmd.is_instance_principal = True if os.getenv(f'{prefix}_INSTANCE_PRINCIPAL') or cmd.is_instance_principal else False
        cmd.is_delegation_token = True if os.getenv(f'{prefix}_DELEGATION_TOKEN') or cmd.is_delegation_token else False
        cmd.force = True if os.getenv(f'{prefix}_FORCE') or cmd.force else False
        cmd.debug = True if os.getenv(f'{prefix}_DEBUG') or cmd.debug else False
        cmd.skip_delete_compartment = True if os.getenv(f'{prefix}_SKIP_DELETE_COMPARTMENT') else False

        # For OCI Functions
        cmd.is_resource_principal = True if os.getenv(f'{prefix}_RESOURCE_PRINCIPAL') else False

        return cmd
    
    # Is a required argument missing? Fail and let the user know
    def validate(self, cmd):
        if not cmd.compartment: return (False, 'compartment')

        return (True, '')
    
    def make_namespace(self) -> argparse.Namespace:
        ns = argparse.Namespace()

        ns.compartment = None
        ns.config_file = None
        ns.config_profile = None
        ns.log_file = None
        ns.regions = None
        ns.objects = None
        ns.threads = -1
        ns.is_instance_principal = None
        ns.is_delegation_token = None
        ns.force = None
        ns.debug = None
        ns.skip_delete_compartment = None

        return ns

    def process(self, cmd):

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
            logging.debug(f'Argument namespace: {cmd}')
            logging.debug(f'Environment variables: {dict(os.environ)}')


        # then process the other arguments
        import oci

        logging.info("Preparing signer")
        # we construct the right signer here
        if cmd.is_instance_principal:
            logging.debug("Authenticating with Instance Principal")
            try:
                self.signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
                self.ociconfig = {
                    'region': self.signer.region,
                    'tenancy': self.signer.tenancy_id
                }

            except Exception:
                errTxt = "Error obtaining instance principals certificate, aborting"
                logging.error(errTxt)
                raise Exception(errTxt)
            
        elif cmd.is_resource_principal:
            logging.debug("Authenticating with Resource Principal")
            try:
                self.signer = oci.auth.signers.get_resource_principals_signer()
                self.ociconfig = {
                    'region': self.signer.region,
                    'tenancy': self.signer.tenancy_id
                }

            except Exception:
                errTxt = "Error obtaining resource princiapl signer, aborting"
                logging.error(errTxt)
                raise Exception(errTxt)

        elif cmd.is_delegation_token:
            logging.debug("Authenticating with Delegation Token")

            delegation_token_location = os.environ["OCI_DELEGATION_TOKEN_FILE"]
            with open(delegation_token_location, 'r') as delegation_token_file:
                delegation_token = delegation_token_file.read().strip()
                # get signer from delegation token
                self.signer = oci.auth.signers.InstancePrincipalsDelegationTokenSigner(delegation_token=delegation_token)

            self.ociconfig = {
                "region"  : os.environ["OCI_REGION"],
                "tenancy" : os.environ["OCI_TENANCY"]
            }

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
        # "set()" filters out dupes - so we only look up the compartment once
        self.compartments = set(cmd.compartment)

        # let's get the compartment info and show it
        self.identity_client = oci.identity.IdentityClient(self.ociconfig, signer=self.signer)
        for compartment in self.compartments:
            try:
                compartment_name = self.identity_client.get_compartment(compartment).data.name
                logging.info("Extirpating resources in compartment '{}' (OCID {})".format(compartment_name, compartment))
                self.all_compartments.append(compartment)
            except:
                logging.error("Failed to get root compartment {}".format(compartment))
                raise Exception

        # then get a list of the child compartments of the compartments
        # I could do this recursively but I like to challenge myself sometimes
        logging.info("Getting child compartments")
        compartments_to_traverse = self.compartments
        while compartments_to_traverse:
            c = compartments_to_traverse.pop()
            logging.debug("Getting child compartments of {}".format(c))
            found = oci.pagination.list_call_get_all_results(self.identity_client.list_compartments,
                                                             c,
                                                             **{
                                                                 "lifecycle_state": "ACTIVE"}
                                                             ).data
            logging.debug( "Found {} child compartments".format( len(found) ) )
            for x in found:
                logging.debug("Found compartment {} with lifecycle_state {}".format(x.id,x.lifecycle_state))

                # this feels redundant - does the search above ever return non-ACTIVE compartments? Hopefully no
                if x.lifecycle_state == "ACTIVE":
                    if x.id in compartments_to_traverse:
                        logging.debug("Compartment {} already in traversal list".format(x.id))
                    else:
                        compartments_to_traverse.add(x.id)

                    if x.id in self.all_compartments:
                        logging.debug("Compartment {} already in 'all compartments' list".format(x.id))
                    else:
                        self.all_compartments.append(x.id)
                else:
                    logging.debug("skipping")
            logging.info("Found {} compartments so far".format( len(self.all_compartments)))

        logging.info("Found a total of {} compartments to extirpate".format(len(self.all_compartments)))

        # regions
        requested_regions = None
        if cmd.regions:
            logging.debug("Regions specified on command line")
            # TODO: make sure that the user doesn't request a region that they aren't subscribed to
            # requested_regions = cmd.regions.split(",")
            self.regions = cmd.regions.split(",")
        else:
            logging.debug("Regions not specified on command line.")

        # cmd.objects should really be catagories. But that ship has sailed
        if cmd.objects:
            catsToDelete = []

            # new feature - allow omitting objects by using a minus sign in front of the name
            if "-" in cmd.objects or "+" in cmd.objects:
                # TODO: allow people to be even more specific!

                # ok so it's important to let users specify an order (for reasons, shut up)
                for cat in cmd.objects.split(","):
                    if cat == "none":
                        # special case
                        logging.debug("special case 'none' for categories")
                        pass
                    if cat == "default":
                        catsToDelete += self.categories_to_delete
                    if cat.startswith("-"):
                        catsToDelete.remove(cat[1:])
                    if cat.startswith("+"):
                        catsToDelete.append(cat[1:])

            else:
                catsToDelete = cmd.objects.split(",")

            self.categories_to_delete = catsToDelete

        logging.info("Getting subscribed regions...")
        regions = self.identity_client.list_region_subscriptions(self.ociconfig["tenancy"]).data
        for region in regions:
            if region.is_home_region:
                self.home_region = region.region_name

            if not cmd.regions:
                self.regions.append( region.region_name )

        logging.info( "Home region: {}".format( self.home_region ) )
        logging.info( "{} Regions to be extirpated: {}".format( len(self.regions), self.regions ) )

        if cmd.threads >= 0:
            # if they give us a limit on number of threads respect it
            self.threads = cmd.threads
        else:
            logging.debug("Setting number of threads to number of regions")
            self.threads = len(self.regions)

        # 1 == 0 for certain values of 1
        if self.threads <= 1:
            self.threads = 0

        logging.info("Number of threads set to {}".format(self.threads))

        if cmd.threads != -1:
            logging.warning("Threading design is under active development and WILL be changed in the future.")

        if cmd.skip_tagged:
            self.skiptagged = self.tagCheck( cmd.skip_tagged )
            # logging.info("Resources tagged with '{}' will be skipped during deletion".format(self.skiptagged))
            logging.info("Resources tagged with '{}' will be skipped during deletion".format(cmd.skip_tagged))

        return
