resource "oci_identity_dynamic_group" "this" {
    compartment_id = var.compartment_ocid
    description = "Dynamic Group for OCIExtirpater Instance"
    name = "${var.label}-dynamic-group"
    matching_rule = "All {instance.id = '${var.instance_ocid}'}"
}

resource "oci_identity_policy" "this" {
    compartment_id = var.compartment_ocid
    description = "Policies for OCIExtirpater"
    name = "${var.label}-policy"
    statements = [
        "Allow dynamic-group ${oci_identity_dynamic_group.this.name} to manage all-resources in compartment id ${var.extirpate_compartment}"
    ]
}