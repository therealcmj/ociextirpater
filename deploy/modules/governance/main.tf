resource "oci_identity_tag_namespace" "this" {
    count = var.use_existing_tag ? 0 : 1

    # Can't be in extirpater cmp due to accidental self-deletion
    compartment_id = var.compartment_ocid
    description = "Tags for extirpater"
    name = "${var.label}-tag-namespace"
}

resource "oci_identity_tag" "this" {
    count = var.use_existing_tag ? 0 : 1

    description = "Extirpater skip deletion"
    name = "Skip"
    tag_namespace_id = oci_identity_tag_namespace.this[0].id
}

resource "time_sleep" "wait_30_seconds" {
    count = var.use_existing_tag ? 0 : 1
    depends_on = [ oci_identity_tag.this ]

    create_duration = "30s"
}