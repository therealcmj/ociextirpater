resource "oci_identity_dynamic_group" "this" {
    # Keeping in root to match default domain
    compartment_id = var.compartment_ocid
    description = "Dynamic Group for OCIExtirpater Instance"
    name = "${var.label}-dynamic-group"
    matching_rule = "All {instance.id = '${var.instance_ocid}'}"
}

resource "oci_identity_policy" "this" {
    compartment_id = var.extirpate_compartment
    description = "Policies for OCIExtirpater"
    name = "${var.label}-policy"
    statements = [
        "Allow dynamic-group ${oci_identity_dynamic_group.this.name} to manage all-resources in compartment id ${var.extirpate_compartment}"
    ]

    defined_tags = {
        "${var.extirpater_tag}" = "True"
    }
}
