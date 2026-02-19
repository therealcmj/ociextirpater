resource "oci_core_vcn" "this" {
  count = var.use_existing_network ? 0 : 1

  compartment_id = var.network_compartment

  cidr_block   = "172.16.0.0/26"
  display_name = "${var.label}-vcn"
  dns_label    = var.label

  freeform_tags = var.extirpater_tag
}

resource "oci_core_subnet" "this" {
  count = var.use_existing_network ? 0 : 1

  compartment_id = var.network_compartment
  cidr_block     = "172.16.0.0/28"
  vcn_id         = oci_core_vcn.this[0].id
  display_name   = "${var.label}-subnet"
  dns_label      = "extirnet"

  route_table_id            = oci_core_route_table.this[0].id
  prohibit_internet_ingress = true
  security_list_ids         = [oci_core_security_list.this[0].id]

  freeform_tags = var.extirpater_tag
}

resource "oci_core_nat_gateway" "this" {
  count = var.use_existing_network ? 0 : 1

  compartment_id = var.network_compartment
  vcn_id         = oci_core_vcn.this[0].id
  display_name   = "${var.label}-nat-gateway"

  freeform_tags = var.extirpater_tag
}

resource "oci_core_service_gateway" "this" {
  count = var.use_existing_network ? 0 : 1

  compartment_id = var.network_compartment
  vcn_id         = oci_core_vcn.this[0].id
  display_name   = "${var.label}-service-gateway"
  #route_table_id = oci_core_route_table.this.id

  services {
    service_id = data.oci_core_services.this.services[0]["id"]
  }

  freeform_tags = var.extirpater_tag
}

resource "oci_core_route_table" "this" {
  count = var.use_existing_network ? 0 : 1

  compartment_id = var.network_compartment
  vcn_id         = oci_core_vcn.this[0].id
  display_name   = "${var.label}-route-table"

  route_rules {
    destination       = "0.0.0.0/0"
    destination_type  = "CIDR_BLOCK"
    network_entity_id = oci_core_nat_gateway.this[0].id
  }

  route_rules {
    destination       = data.oci_core_services.this.services[0]["cidr_block"]
    destination_type  = "SERVICE_CIDR_BLOCK"
    network_entity_id = oci_core_service_gateway.this[0].id
  }

  freeform_tags = var.extirpater_tag
}

resource "oci_core_security_list" "this" {
  count = var.use_existing_network ? 0 : 1

  compartment_id = var.network_compartment
  vcn_id         = oci_core_vcn.this[0].id
  display_name   = "${var.label}-security-list"

  egress_security_rules {
    destination      = data.oci_core_services.this.services[0]["cidr_block"]
    destination_type = "SERVICE_CIDR_BLOCK"
    protocol         = "all"
  }

  egress_security_rules {
    destination      = "0.0.0.0/0"
    destination_type = "CIDR_BLOCK"
    protocol         = "all"
  }

  ingress_security_rules {
    description = "Local SSH access for Cloud Shell"
    protocol    = "6"
    source      = "172.16.0.0/26"
    source_type = "CIDR_BLOCK"

    tcp_options {
      min = 22
      max = 22
    }
  }

  freeform_tags = var.extirpater_tag
}