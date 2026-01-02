locals {
    resources_compartment = length(var.deployment_compartment) > 0 ? var.deployment_compartment : var.cleanup_compartment
}