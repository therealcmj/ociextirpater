resource "oci_core_instance" "this" {
  compartment_id       = var.compute_compartment
  display_name         = "${var.label}-instance"
  preserve_boot_volume = false

  #Network
  # random_integer is an integer between 0 and the number of availability domains - 1
  # The AD is chosen at random rather than trying to put all computes in any single AD
  availability_domain = data.oci_identity_availability_domains.this.availability_domains[random_integer.ad.result].name
  create_vnic_details {
    subnet_id        = var.subnet_ocid
    assign_public_ip = false
  }

  instance_options {
    are_legacy_imds_endpoints_disabled = true
  }

  shape = "VM.Standard.E5.Flex"

  shape_config {
    memory_in_gbs = 6
    ocpus         = 1
  }

  source_details {
    source_id   = data.oci_core_images.this.images[0].id
    source_type = "image"
  }

  metadata = {
    ssh_authorized_keys = var.ssh_public_key == null ? "" : var.ssh_public_key
    user_data = base64encode(format("#!/bin/bash\n%s\n%s\n%s",
      "TOBEDELETED=${var.extirpate_compartment}",
      "EXT_TAG=${local.key}=${var.extirpater_tag[local.key]}",
    file("./scripts/bootstrap.sh")))
  }

  freeform_tags = var.extirpater_tag
}

resource "random_integer" "ad" {
  min = 0
  //max = length(data.oci_identity_availability_domains.this.availability_domains) - 1
  max = data.oci_identity_availability_domains.this.availability_domains != null ? length(data.oci_identity_availability_domains.this.availability_domains) - 1 : 0
}
