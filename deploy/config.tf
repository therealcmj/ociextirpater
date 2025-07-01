module "network" {
  source         = "./modules/network"
  compartment_ocid = var.compartment_id
  label = var.label
  existing_vcn = var.existing_vcn
  existing_subnet = var.existing_subnet
  use_existing_network = var.use_existing_network
}

module "compute" {
  source        = "./modules/compute"
  compartment_ocid = var.compartment_id
  label = var.label
  subnet_ocid = module.network.subnet_ocid
  ssh_public_key = var.ssh_public_key
  extirpate_compartment = var.cleanup_compartment
}

module "iam" {
  source        = "./modules/iam"
  label = var.label
  compartment_ocid = var.tenancy_ocid
  extirpate_compartment = var.cleanup_compartment
  instance_ocid = module.compute.instance_ocid
}