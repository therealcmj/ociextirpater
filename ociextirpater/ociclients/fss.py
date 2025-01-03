import logging

import oci
from ociextirpater.OCIClient import OCIClient

class fss( OCIClient ):
    service_name = "Filesystem Service"
    clientClass = oci.file_storage.FileStorageClient

    # we are going to need the ADs for each region
    # while I feel like I *should* do that up at a higher level FSS seems to be the only service that needs that info
    # so for now I'm going to implement this here. Even though it means I have to do some suboptimal stuff
    regionADs = {}

    objects = [
        {
            "name_singular"      : "File System",
            "name_plural"        : "File Systems",
            "formatter"          : lambda filesystem: "Filesystem with OCID {} / name '{}' is in state {}".format(filesystem.id, filesystem.display_name, filesystem.lifecycle_state),
            "function_list"      : "list_file_systems",
            "function_delete"    : "delete_file_system",
        },

        # Export Sets doesn't have a delete_export_set
        # {
        #     "name_singular"      : "Export Set",
        #     "name_plural"        : "Export Sets",
        #
        #     "function_list"      : "list_export_sets",
        #     "function_delete"    : "delete_export_set",
        # },

        {
            "name_singular"      : "Export",
            "name_plural"        : "Exports",

            "function_list"      : "list_exports",
            "function_delete"    : "delete_export",
        },

        {
            "name_singular"      : "Mount Target",
            "name_plural"        : "Mount Targets",

            "function_list"      : "list_mount_targets",
            "function_delete"    : "delete_mount_target",
        },

        {
            "name_singular"      : "Outbound Connector",
            "name_plural"        : "Outbound Connectors",
            "function_list"      : "list_outbound_connectors",
            "function_delete"    : "delete_outbound_connector",
        },

        {
            "name_singular"      : "Replication Target",
            "name_plural"        : "Replication Targets",
            "function_list"      : "list_replication_targets",
            "function_delete"    : "delete_replication_target",
        },

        {
            "name_singular"      : "Replication",
            "name_plural"        : "Replications",
            "function_list"      : "list_replications",
            "function_delete"    : "delete_replication",
        },

        {
            "name_singular"      : "Filesystem Snapshot Policy",
            "name_plural"        : "Filesystem Snapshot Policies",
            "function_list"      : "list_filesystem_snapshot_policies",
            "function_delete"    : "delete_filesystem_snapshot_policy",
        },

        {
            "name_singular"      : "Snapshot",
            "name_plural"        : "Snapshots",
            "function_list"      : "list_snapshots",
            "function_delete"    : "delete_snapshot",
        },

        # {
        #     "name_singular"      : "XXX",
        #     "name_plural"        : "XXXXs",
        #     "checkIt"            : lambda image: hasattr(image, "compartment_id") and image.compartment_id != None,

        #     "function_list"      : "list_xxx",
        #     "kwargs_list"        : {
        #                            },
        #     "formatter"          : lambda instance: "XXX instance with OCID {} / name '{}' is in state {}".format( instance.id, instance.name, instance.lifecycle_state ),
        #     "function_delete"    : "delete_xxx",
        # },
    ]

    def __init__(self,config):
        for region in config.regions:
            logging.info("Getting ADs for region {}".format(region))
            import oci.identity.identity_client
            rconfig = config.ociconfig
            rconfig["region"] = region
            idc = oci.identity.identity_client.IdentityClient( rconfig, signer=config.signer )

            r = idc.list_availability_domains( rconfig["tenancy"] )

            # logging.debug("R.data = {}".format(r.data))
            self.regionADs[region] = r.data
        super().__init__(config)

    # FSS requires you to check each AD separately
    #
    # NOTE: I am trying overriding findAllInCompartment instead of the old and unloved "list_objects" thing I did first
    #       If this works well I'll switch those implementations
    def findAllInCompartment(self, region, o, this_compartment, **kwargs):
        total_result = []

        if o["name_plural"] == "Exports" or o["name_plural" == "Snapshots"]:
            kwargs = {
                "compartment_id": this_compartment
            }
            x = oci.pagination.list_call_get_all_results(getattr((self.clients[region]), o["function_list"]),
                                                         **kwargs).data

            logging.debug("Found {} {}".format(len(x), o["name_plural"]))
            for y in x:
                total_result.append(y)
        else:

            for ad in self.regionADs[region]:
                logging.debug("Checking in AD {} / {}".format(ad.name, ad.id))
                x = oci.pagination.list_call_get_all_results(getattr((self.clients[region]), o["function_list"]),
                                                              this_compartment,
                                                              ad.name,
                                                              **kwargs).data

                logging.debug("Found {} {} in AD {}".format( len(x), o["name_plural"], ad.name) )
                for y in x:
                    total_result.append(y)

        logging.debug("Total of {} {} in compartment {} in region {}".format( len( total_result), o["name_plural"],this_compartment, region ))
        return total_result
