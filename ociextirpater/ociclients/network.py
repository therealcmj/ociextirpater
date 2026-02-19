import logging

import oci
from ociextirpater.OCIClient import OCIClient

class network( OCIClient ):
    service_name = "Networking"
    clientClass = oci.core.VirtualNetworkClient
    compositeClientClass = oci.core.VirtualNetworkClientCompositeOperations

    objects = [
        # we are going to do Network route tables twice
        # the first time through we remove the entries (during the pre-delete phase)
        # BUT we can't delete the route table at that point because you can't delete the default route table from a VCN
        {
            "function_list": "list_route_tables",
            # "function_delete": "delete_route_table",
            "name_singular": "Networking route table",
            "name_plural": "Networking route tables",
        },

        # then try to get rid of the subnets
        {
            "function_list": "list_subnets",
            "function_delete"    : "delete_subnet",
            "name_singular"      : "Subnet",
            "name_plural"        : "Subnets",
            "children"           : [
                                    {
                                        "function_list"      : "list_ipv6s",
                                        "function_delete"    : "delete_ipv6",
                                        "name_singular"      : "Private IPv6 IP",
                                        "name_plural"        : "Private IPv6 IPs",
                                    },
                                    {
                                        "function_list"      : "list_xxx",
                                        "function_delete"    : "delete_private_ip",
                                        "name_singular"      : "private IP",
                                        "name_plural"        : "private IPs",
                                    }]
        },
        {
            "function_list"      : "list_dhcp_options",
            "function_delete"    : "delete_dhcp_options",
            "name_singular"      : "DHCP options",
            "name_plural"        : "Sets of DHCP options",
        },

        {
            "function_list"      : "list_service_gateways",
            "function_delete"    : "delete_service_gateway",
            "name_singular"      : "service gateway",
            "name_plural"        : "service gateways",
        },

        {
            "function_list"      : "list_remote_peering_connections",
            "function_delete"    : "delete_remote_peering_connection",
            "name_singular"      : "Remote peering connection",
            "name_plural"        : "Remote peering connections",
        },

        {
            "function_list"      : "list_nat_gateways",
            "function_delete"    : "delete_nat_gateway",
            "name_singular"      : "NAT gateway",
            "name_plural"        : "NAT gateways",
        },

        {
            "function_list"      : "list_local_peering_gateways",
            "function_delete"    : "delete_local_peering_gateway",
            "name_singular"      : "local peering gateway",
            "name_plural"        : "local peering gateways",
        },


        {
            "function_list"      : "list_internet_gateways",
            "function_delete"    : "delete_internet_gateway",
            "name_singular"      : "internet gateway",
            "name_plural"        : "internet gateways",
        },

        {
            "function_list"      : "list_virtual_circuits",
            "function_delete"    : "delete_virtual_circuit",
            "name_singular"      : "Virtual Circuit",
            "name_plural"        : "Virtual Circuits",
        },

        {
            # must not be mapped to a VirtualCircuit
            "function_list"      : "list_cross_connects",
            "function_delete"    : "delete_cross_connect",
            "name_singular"      : "Networking cross conntect",
            "name_plural"        : "Networking cross conntects",
        },

        {
            "function_list"      : "list_ip_sec_connections",
            "function_delete"    : "delete_ip_sec_connection",
            "name_singular"      : "IPSec connection",
            "name_plural"        : "IPSec connections",
        },

        {
            "function_list"      : "list_drg_attachments",
            "function_delete"    : "delete_drg_attachment",
            "name_singular"      : "Networking DRG attachment",
            "name_plural"        : "Networking DRG attachments",
        },
        {
            "function_list"      : "list_drgs",
            "function_delete"    : "delete_drg",
            "name_singular"      : "Networking DRG",
            "name_plural"        : "Networking DRGs",
        },
        {
            # The CPE must not be connected to a DRG
            # but we already did those so we're good
            "function_list"      : "list_cpes",
            "function_delete"    : "delete_cpe",
            "formatter"          : lambda instance: "CPE with OCID {} / name '{}'".format( instance.id, instance.display_name),

            "name_singular"      : "Networking CPE",
            "name_plural"        : "Networking CPEs",
        },
        {
            "function_list"      : "list_capture_filters",
            "function_delete"    : "delete_capture_filter",
            "name_singular"      : "Networking capture filter",
            "name_plural"        : "Networking capture filters",
        },

        {
            "function_list"      : "list_byoip_ranges",
            "function_delete"    : "delete_byoip_range",
            "name_singular"      : "BYO IP range",
            "name_plural"        : "BYO IP ranges",
        },

        {
            "function_list"      : "list_public_ip_pools",
            "function_delete"    : "delete_public_ip_pool",
            "name_singular"      : "public IP pool",
            "name_plural"        : "public IP pools",
        },

        {
            # "function_list"      : "list_public_ips",
            "function_delete"    : "delete_public_ip",
            "name_singular"      : "public IP",
            "name_plural"        : "public IPs",
        },

        # then try to get rid of the subnets
        # this will take care of the default route table associated for the subnet
        {
            "function_list"      : "list_subnets",
            "function_delete"    : "delete_subnet",
            "name_singular"      : "Subnet",
            "name_plural"        : "Subnets",
        },

        # now get any extra (i.e. not default) route tables
        {
            "function_list"      : "list_route_tables",
            "function_delete"    : "delete_route_table",
            "name_singular"      : "Networking route table",
            "name_plural"        : "Networking route tables",
        },
        {
            "function_list"      : "list_vlans",
            "function_delete"    : "delete_vlan",
            "name_singular"      : "Virtual LAN",
            "name_plural"        : "Virtual LANs",
        },

        {
            "function_list"      : "list_vcns",
            "function_delete"    : "delete_vcn",
            "name_singular"      : "VCN",
            "name_plural"        : "VCNs",
        },

        {
            "function_list"      : "list_security_lists",
            "function_delete"    : "delete_security_list",
            "name_singular"      : "Networking security list",
            "name_plural"        : "Networking security lists",
        },

        {
            # "function_list"      : "list_xxx",
            "function_delete"      : "delete_network_security_group",
            "name_singular"        : "Network Security Group",
            "name_plural"          : "Network Security Groups",
        },

        # {
        #     # "formatter"          : lambda instance: "XXX instance with OCID {} / name '{}' is in state {}".format( instance.id, instance.name, instance.lifecycle_state ),
        #     "function_list"      : "list_xxx",
        #     "kwargs_list"        : {
        #                            },
        #     "function_delete"    : "delete_xxx",
        #     "name_singular"      : "XXX",
        #     "name_plural"        : "XXXXs",
        # },
    ]

    def predelete(self,object,region,found_object):
        # we have pre-delete work to do in case of a route table
        if object["name_plural"] == "Networking route tables":
            f = getattr((self.clients[region]), "update_route_table")
            logging.debug("Updating route table to remove existing route rules")
            newrules = oci.core.models.UpdateRouteTableDetails(
                **{
                    "route_rules":[]
                }
            )
            f( found_object.id, newrules, **{})

    def list_objects(self, o, region, this_compartment, **kwargs):
        if o["name_plural"] == "Network Security Groups":
            return oci.pagination.list_call_get_all_results(
                getattr((self.clients[region]), "list_network_security_groups"),
                **{"compartment_id":this_compartment}).data

        elif o["name_plural"] == "public IPs":
            return oci.pagination.list_call_get_all_results(getattr((self.clients[region]), "list_public_ips"),"REGION",this_compartment,**{}).data

        # elif o["name_plural"] == "ADM Knowledge Bases":
        #     return oci.pagination.list_call_get_all_results(
        #         getattr((self.clients[region]), "list_knowledge_bases"),
        #         **{"compartment_id": this_compartment}).data
        else:
            raise NotImplementedError


    def delete_object(self, object, region, found_object):
        if object["name_plural"] == "VCNs":
            self.compositeClients[region].delete_vcn_and_wait_for_state(found_object.id,wait_for_states=[oci.core.models.Vcn.LIFECYCLE_STATE_TERMINATED])
            return

        raise NotImplementedError
