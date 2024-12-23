import oci
from ociextirpater.OCIClient import OCIClient

class blockstorage( OCIClient ):
    service_name = "Block Storage"
    clientClass = oci.core.BlockstorageClient

    def list_objects(self, o, region, this_compartment, **kwargs):
        if o["name_plural"] == "Boot Volume Replicas":
            return oci.pagination.list_call_get_all_results(
                getattr((self.clients[region]), "list_boot_volume_replicas"),
                **{"compartment_id":this_compartment}).data

        if o["name_plural"] == "Boot Volumes":
            return oci.pagination.list_call_get_all_results(
                getattr((self.clients[region]), "list_boot_volumes"),
                **{"compartment_id":this_compartment}).data

        if o["name_plural"] == "Block Volume Replicas":
            return oci.pagination.list_call_get_all_results(
                getattr((self.clients[region]), "list_block_volume_replicas"),
                **{"compartment_id":this_compartment}).data

        if o["name_plural"] == "Block Volume Backup Policies":
            return oci.pagination.list_call_get_all_results(
                getattr((self.clients[region]), "list_volume_backup_policies"),
                **{"compartment_id":this_compartment}).data

        if o["name_plural"] == "Volumes":
            return oci.pagination.list_call_get_all_results(
                getattr((self.clients[region]), "list_volumes"),
                **{"compartment_id":this_compartment}).data

        raise NotImplementedError

    objects = [
        {
            "function_list"      : "list_boot_volume_backups",
            "function_delete"    : "delete_boot_volume_backup",
            "name_singular"      : "Boot Volume Backup",
            "name_plural"        : "Boot Volume Backups",
        },

        {
            "function_list"      : "list_boot_volume_replicas",
            "function_delete"    : "delete_boot_volume_replica",
            "name_singular"      : "Boot Volume Replica",
            "name_plural"        : "Boot Volume Replicas",
        },

        {
            "function_list": "list_boot_volumes",
            "function_delete": "delete_boot_volume",
            "name_singular": "Boot Volume",
            "name_plural": "Boot Volumes",
        },

        {
            "function_list"      : "list_block_volume_replicas",
            "function_delete"    : "delete_block_volume_replicas",
            "name_singular"      : "Block Volume Replica",
            "name_plural"        : "Block Volume Replicas",
        },

        {
            "function_list"      : "list_volume_backup_policies",
            "function_delete"    : "delete_volume_backup_policy",
            "name_singular"      : "Block Volume Backup Policy",
            "name_plural"        : "Block Volume Backup Policies",
        },

        {
            "function_list"      : "list_volume_backups",
            "function_delete"    : "delete_volume_backup",
            "name_singular"      : "Volume Backup",
            "name_plural"        : "Volume Backups",
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
