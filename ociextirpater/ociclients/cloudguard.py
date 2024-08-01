import oci
from ociextirpater.OCIClient import OCIClient

class cloudguard( OCIClient ):
    service_name = "Cloud Guard"
    clientClass = oci.cloud_guard.CloudGuardClient

    objects = [
        {
            "function_list"      : "list_security_zones",
            "function_delete"    : "delete_security_zone",
            "name_singular"      : "Security Zone",
            "name_plural"        : "Security Zones",
        },

        {
            "name_singular"      : "Cloud Guard Target",
            "name_plural"        : "Cloud Guard Targets",
            "function_list"      : "list_targets",
            "function_delete"    : "delete_target",
        },

        # if you enable this you will get this error:
        # 'DataMaskRule is root compartment level entity, will be listed for root compartment only. '
        # {
        #     "name_singular"      : "Cloud Guard Data Mask Rule",
        #     "name_plural"        : "Cloud Guard Data Mask Rules",
        #     "function_list"      : "list_data_mask_rules",
        #     "function_delete"    : "delete_data_mask_rule",
        # },

        {
            "name_singular"      : "Cloud Guard Data Source",
            "name_plural"        : "Cloud Guard Data Sources",
            "function_list"      : "list_data_sources",
            "function_delete"    : "delete_data_source",
        },

        {
            "name_singular"      : "Cloud Guard Detector Recipe",
            "name_plural"        : "Cloud Guard Detector Recipes",
            "function_list"      : "list_detector_recipes",
            "function_delete"    : "delete_detector_recipe",
        },

        {
            "name_singular"      : "Cloud Guard Managed List",
            "name_plural"        : "Cloud Guard Managed Lists",
            "function_list"      : "list_managed_lists",
            "function_delete"    : "delete_managed_list",
        },

        {
            "name_singular"      : "Cloud Guard Responder Recipe",
            "name_plural"        : "Cloud Guard Responder Recipes",
            "function_list"      : "list_responder_recipes",
            "function_delete"    : "delete_responder_recipe",
        },

        {
            "name_singular"      : "Cloud Guard Security Recipe",
            "name_plural"        : "Cloud Guard Security Recipes",
            "check2delete"       : lambda recipe: hasattr(recipe, "owner") and recipe.owner != "ORACLE",

            "function_list"      : "list_security_recipes",
            "function_delete"    : "delete_security_recipe",
        },

        {
            "name_singular"      : "Cloud Guard Security Zone",
            "name_plural"        : "Cloud Guard Security Zones",
            "function_list"      : "list_security_zones",
            "function_delete"    : "delete_security_zone",
        },

        # list here takes list_target_detector_recipes(self, target_id, compartment_id, **kwargs):
        # TODO: come back ot that and see if we even need to implement this
        # {
        #     "name_singular"      : "Cloud Guard Target Detector Recipe",
        #     "name_plural"        : "Cloud Guard Target Detector Recipes",
        #     "function_list"      : "list_target_detector_recipes",
        #     "function_delete"    : "delete_target_detector_recipe",
        # },

        # {
        #     "name_singular"      : "Cloud Guard Target Responder Recipe",
        #     "name_plural"        : "Cloud Guard Target Responder Recipes",
        #     "function_list"      : "list_target_responder_recipes",
        #     "function_delete"    : "delete_target_responder_recipe",
        # },

        # {
        #     "name_singular"      : "Cloud Guard XXX",
        #     "name_plural"        : "Cloud Guard XXXs",
        #     "function_list"      : "XXX",
        #     "function_delete"    : "XXX",
        # },

    ]


