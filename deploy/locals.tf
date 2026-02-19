locals {
  resources_compartment = var.use_deployment_compartment && var.deployment_compartment != null && length(var.deployment_compartment) > 0 ? var.deployment_compartment : var.cleanup_compartment
  networks_compartment  = var.network_compartment != null && length(var.network_compartment) > 0 ? var.network_compartment : local.resources_compartment
}