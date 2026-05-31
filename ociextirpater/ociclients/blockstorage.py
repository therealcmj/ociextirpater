import logging
import oci
from ociextirpater.OCIClient import OCIClient

from inspect import signature


class blockstorage( OCIClient ):
    service_name = "Block Storage"
    clientClass = oci.core.BlockstorageClient
    compositeClientClass = oci.core.BlockstorageClientCompositeOperations

    objects = [
        {
            "name_singular"      : "Block Volume Group",
            "name_plural"        : "Block Volume Groups",
            "function_list"      : "list_volume_groups",
            "function_delete"    : "delete_volume_group",
        },

        {
            "name_singular"      : "Block Volume Backup Policy",
            "name_plural"        : "Block Volume Backup Policies",
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
            "name_singular"      : "Boot Volume Backup",
            "name_plural"        : "Boot Volume Backups",
            "function_list"      : "list_boot_volume_backups",
            "function_delete"    : "delete_boot_volume_backup",
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
            "name_singular"      : "Block Volume Backup",
            "name_plural"        : "Block Volume Backups",
            "function_list"      : "list_volume_backups",
            "function_delete"    : "delete_volume_backup",
        },

        {
            "name_singular"      : "Block Volume Group Replica",
            "name_plural"        : "Block Volume Group Replicas",
            "function_list"      : "list_volume_group_replicas",
            "function_delete"    : "volume_group_replica",
        },

        {
            "name_singular"      : "Block Volume Group Backup",
            "name_plural"        : "Block Volume Group Backups",
            "function_list"      : "list_volume_group_backups",
            "function_delete"    : "delete_volume_group_backup",
        },

        {
            "name_singular"      : "Block Volume Group",
            "name_plural"        : "Block Volume Groups",
            "function_list"      : "list_volume_groups",
            "function_delete"    : "delete_volume_group",
        },

        {
            "name_singular"      : "Block Volume",
            "name_plural"        : "Block Volumes",
            "function_list"      : "list_volumes",
            "function_delete"    : "delete_volume",
        },
    ]

    def findAllInCompartment(self, region, o, this_compartment, **kwargs):
        funcname = o["function_list"]
        f = getattr(self.clients[region], funcname)

        sig = signature(f)
        params = []
        for name, param in sig.parameters.items():
            # logging.debug("Function param: name={} type: {}".format(name,param.kind))
            params.append(name)

        # TODO (far) in the future: move this up into OCIClient
        if params[0] == "compartment_id":
            logging.debug("Method {} takes compartment_id as first parameter".format(funcname))
            return oci.pagination.list_call_get_all_results(
                f,
                this_compartment).data
        
        elif params[0] == "availability_domain" and params[1] == "compartment_id":        
            logging.debug("Method {} takes availability_domain, compartment_id as parameters".format(funcname))
            ret=[]
            for ad in self.get_availability_domains(region):
                logging.debug("Getting {} in region {} AD {}".format(o["name_plural"],region,ad.name))
                adres = oci.pagination.list_call_get_all_results(
                    f,
                    ad.name,
                    this_compartment,
                    **{}
                ).data
                logging.debug("AD {} returned {} {}".format(ad.name, len(adres), o["name_plural"]))
                ret.extend(adres)
            return ret

        elif params[0] == "kwargs":
            logging.debug("Method {} takes compartment_id in the kwargs".format(funcname))
            return oci.pagination.list_call_get_all_results(
                f,
                **{"compartment_id":this_compartment}).data

        logging.warning("Calling super() method to find all resource in compartment.")
        return super().findAllInCompartment(self,region, o, this_compartment, **kwargs)

    def delete_object(self, object, region, found_object):

        if object["name_plural"] == "Boot Volumes":
            logging.debug("Checking Boot Volume for replicas")

            if not hasattr( found_object, "boot_volume_replicas") or found_object.boot_volume_replicas == None:
                logging.debug("Boot volume does not have any replicas.")
            else:
                logging.debug("Block volume has {} replica(s)".format(len(found_object.boot_volume_replicas)))

                f = getattr(self.compositeClients[region], "update_boot_volume_and_wait_for_state")
                logging.debug("Updating boot volume to remove replicas")
                f(
                    found_object.id,
                    oci.core.models.UpdateBootVolumeDetails(
                        boot_volume_replicas=[]
                    ),
                    [
                        oci.core.models.Volume.LIFECYCLE_STATE_AVAILABLE,
                        # oci.core.models.Volume.LIFECYCLE_STATE_FAULTY
                    ]
                )
                logging.debug("Done.")


        elif object["name_plural"] == "Block Volumes":
            logging.debug("Checking Block Volume for replicas")

            if not hasattr( found_object, "block_volume_replicas") or found_object.block_volume_replicas == None:
                logging.debug("Block volume does not have any replicas.")
            else:
                logging.debug("Block volume has {} replica(s)".format(len(found_object.block_volume_replicas)))

                f = getattr(self.compositeClients[region], "update_volume_and_wait_for_state")
                logging.debug("Updating volume to remove replicas")
                f(
                    found_object.id,
                    oci.core.models.UpdateVolumeDetails(
                        block_volume_replicas=[]
                    ),
                    [
                        oci.core.models.Volume.LIFECYCLE_STATE_AVAILABLE,
                        # oci.core.models.Volume.LIFECYCLE_STATE_FAULTY
                    ]
                )
                logging.debug("Done.")

        elif object["name_plural"] == "Volume Groups":
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

        logging.debug("Calling super().delete_object() to delete")
        return super().delete_object(object, region, found_object)
