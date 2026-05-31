import logging
import oci
from ociextirpater.OCIClient import OCIClient

class legacyNWFWClient( OCIClient ):
    service_name = "Legacy Network Firewall"
    clientClass = oci.network_firewall.NetworkFirewallClient
    
    def __init__(self, config):
        super().__init__(config)
        for client in self.clients.values():
            client.base_client._base_path = "/20211001"
            client.base_client.endpoint = client.base_client.endpoint.replace("/20230501","/20211001")
    

class nwfw( OCIClient ):
    service_name = "Network Firewall"
    clientClass = oci.network_firewall.NetworkFirewallClient
    _legacy_client = None

    objects = [
        {
            "name_singular"      : "Legacy Network Firewall",
            "name_plural"        : "Legacy Network Firewalls",
            "function_list"      : "list_network_firewalls",
            "function_delete"    : "delete_network_firewall",
        },

        {
            "name_singular"      : "Legacy Network Firewall Policy",
            "name_plural"        : "Legacy Network Firewall Policies",
            "function_list"      : "list_network_firewall_policies",
            "function_delete"    : "delete_network_firewall_policy",
        },

        {
            "name_singular"      : "Network Firewall",
            "name_plural"        : "Network Firewalls",
            "function_list"      : "list_network_firewalls",
            "function_delete"    : "delete_network_firewall",
        },

        {
            "name_singular"      : "Network Firewall Policy",
            "name_plural"        : "Network Firewall Policies",
            "function_list"      : "list_network_firewall_policies",
            "function_delete"    : "delete_network_firewall_policy",
        },

    ]

    def __init__(self,config):
        # call the super
        super().__init__(config)

        # then, because v1 NWFWs are not in the SDK any more do our own
        self._legacy_client = legacyNWFWClient( config )

    def findAllInCompartment(self, region, o, this_compartment, **kwargs):
        if o["name_plural"].startswith("Legacy "):
            r = self._legacy_client.findAllInCompartment( region, o, this_compartment, **kwargs)
            return r
        else:
            return super().findAllInCompartment(region, o, this_compartment, **kwargs)

    def delete_object(self, object, region, found_object):
        if object["name_plural"].startswith("Legacy "):
            logging.warning( "Deleting legacy NWFW - this code is extremely lightly tested. If you see this message please report back on success/failure!" )

            f = getattr((self._legacy_client.clients[region]), object.get("function_delete"))
            logging.info( "Deleting {}".format(object.get("name_singular")) )
            f( found_object.id )
            return
    
        return super().delete_object(object, region, found_object)
