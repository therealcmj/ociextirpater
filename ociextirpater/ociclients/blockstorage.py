import logging
import oci
from ociextirpater.OCIClient import OCIClient

class blockstorage( OCIClient ):
    service_name = "Block Storage"
    clientClass = oci.core.BlockstorageClient
    # compositeClientClass = oci.core.BlockstorageClientCompositeOperations

    def list_objects(self, o, region, this_compartment, **kwargs):
        # Boot and Block Volumes have different methods
        if o["name_plural"] == "Boot Volumes":
            return oci.pagination.list_call_get_all_results(
                getattr((self.clients[region]), "list_boot_volumes"),
                **{"compartment_id":this_compartment}).data

        if o["name_plural"] == "Boot Volume Replicas":
            return oci.pagination.list_call_get_all_results(
                getattr((self.clients[region]), "list_boot_volume_replicas"),
                **{"compartment_id":this_compartment}).data


        if o["name_plural"] == "Volumes":
            return oci.pagination.list_call_get_all_results(
                getattr((self.clients[region]), "list_volumes"),
                **{"compartment_id":this_compartment}).data

        if o["name_plural"] == "Block Volume Replicas":
            return oci.pagination.list_call_get_all_results(
                getattr((self.clients[region]), "list_block_volume_replicas"),
                **{"compartment_id":this_compartment}).data


        # Volume Backup policies are common to both Boot and Block volumes
        if o["name_plural"] == "Volume Backup Policies":
            return oci.pagination.list_call_get_all_results(
                getattr((self.clients[region]), "list_volume_backup_policies"),
                **{"compartment_id":this_compartment}).data

        raise NotImplementedError

    objects = [
        {
            "name_singular"      : "Volume Group",
            "name_plural"        : "Volume Groups",
            "function_list"      : "list_volume_groups",
            "function_delete"    : "delete_volume_group",
        },

        {
            "name_singular"      : "Volume Backup Policy",
            "name_plural"        : "Volume Backup Policies",
            "function_list"      : "list_volume_backup_policies",
            "formatter"          : lambda policy: "Block Volume Backup Policy with OCID {} / display name '{}'".format(policy.id, policy.display_name),
            "function_delete"    : "delete_volume_backup_policy",
        },

        # {
        #     "function_list"      : "list_block_volume_replicas",
        #     "function_delete"    : "delete_block_volume_replicas",
        #     "name_singular"      : "Block Volume Replica",
        #     "name_plural"        : "Block Volume Replicas",
        # },

        {
            "function_list"      : "list_boot_volume_backups",
            "function_delete"    : "delete_boot_volume_backup",
            "name_singular"      : "Boot Volume Backup",
            "name_plural"        : "Boot Volume Backups",
        },

        # {
        #     "function_list"      : "list_boot_volume_replicas",
        #     "function_delete"    : "delete_boot_volume_replica",
        #     "name_singular"      : "Boot Volume Replica",
        #     "name_plural"        : "Boot Volume Replicas",
        # },

        {
            "name_singular"      : "Boot Volume",
            "name_plural"        : "Boot Volumes",
            "function_list"      : "list_boot_volumes",
            "function_delete"    : "delete_boot_volume",
        },

        {
            "name_singular"      : "Volume Backup",
            "name_plural"        : "Volume Backups",
            "function_list"      : "list_volume_backups",
            "function_delete"    : "delete_volume_backup",
        },

        # this is harder because the function signature is
        # list_volume_group_replicas(availability_domain, compartment_id, **kwargs)
        # {
        #     "function_list"      : "list_volume_group_replicas",
        #     "kwargs_list"        : {
        #                            },
        #     "function_delete"    : "volume_group_replica",
        #     "name_singular"      : "Volume Group Replica",
        #     "name_plural"        : "Volume Group Replicas",
        # },

        {
            "function_list"      : "list_volume_group_backups",
            "function_delete"    : "delete_volume_group_backup",
            "name_singular"      : "Volume Group Backup",
            "name_plural"        : "Volume Group Backups",
        },

        {
            "function_list"      : "list_volume_groups",
            "function_delete"    : "delete_volume_group",
            "name_singular"      : "Volume Group",
            "name_plural"        : "Volume Groups",
        },

        {
            "function_list"      : "list_volumes",
            "function_delete"    : "delete_volume",
            "name_singular"      : "Volume",
            "name_plural"        : "Volumes",
        },
    ]

    def predelete(self,object,region,found_object):
        logging.debug("In pre-delete method")

        # No pre-delete needed here
        # # TODO: fix the OCIClient to not abort on NotImplementedException and then remove these
        # if object["name_plural"] == "Boot Volume Backups":
        #     #NO OP here
        #     return
        #
        # if object["name_plural"] == "Volume Backup Policies":
        #     #NO OP here
        #     return


        if object["name_plural"] == "Boot Volumes":
            if not hasattr( found_object, "boot_volume_replicas") or found_object.boot_volume_replicas == None:
                logging.debug("Boot volume doesn't have any replicas.")
                return

            f = getattr((self.clients[region]), "update_boot_volume")
            logging.info("Updating boot volume")
            f(
                found_object.id,
                oci.core.models.UpdateBootVolumeDetails(
                    boot_volume_replicas=None
                )
            )
            return

        if object["name_plural"] == "Block Volumes":
            if not hasattr( found_object, "volume_replicas") or found_object.volume_replicas == None:
                logging.debug("Boot volume doesn't have any replicas.")
                return

            f = getattr((self.clients[region]), "update_volume")
            logging.info("Updating volume")
            f(
                found_object.id,
                {
                    "block_volume_replicas": None
                }
            )
            return

        if object["name_plural"] == "Volume Groups":
            f = getattr((self.clients[region]), "update_volume_group")
            logging.info("Updating volume group")
            f(
                found_object.id,
                {
                   "volume_group_replicas": [],
                   "volume_ids": []
                },
                **{
                   "preserve_volume_replica": False,
                }
            )
            return

        raise NotImplementedError
