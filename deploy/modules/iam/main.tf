resource "oci_identity_dynamic_group" "this" {
  # Keeping in root to match default domain
  compartment_id = var.root_compartment
  description    = "Dynamic Group for OCIExtirpater Instance"
  name           = "${var.label}-dynamic-group"
  matching_rule  = "All {instance.id = '${var.instance_ocid}'}"
}

resource "oci_identity_policy" "extirpate" {
  compartment_id = var.deploy_in_root ? var.root_compartment : var.extirpate_compartment
  description    = "Policies for OCIExtirpater"
  name           = "${var.label}-policy"
  statements     = concat(local.dynamic_group_statements, local.scheduler_statements)

  freeform_tags = var.extirpater_tag
}
