import logging

import oci
from ociexterpater.OCIClient import OCIClient

class dns( OCIClient ):
    service_name = "DNS"
    clientClass = oci.dns.DnsClient

    objects = [
        # {
        #     "function_list"      : "list_resolvers",
        #     "kwargs_list"        : {
        #                            },
        #     "function_delete"    : "delete_xxx",
        #     "name_singular"      : "XXX",
        #     "name_plural"        : "XXXXs",
        # },
        {
            "formatter"          : lambda resolver_endpoint: "DNS Resolver Endpoint name '{}' in DNS Resolver {}".format( resolver_endpoint.name, resolver_endpoint.endpoint_id ),
            # "function_list"      : "list_resolver_endpoints",
            # "function_delete"    : "delete_resolver_endpoint",
            "name_singular"      : "DNS Resolver Endpoint",
            "name_plural"        : "DNS Resolver Endpoints",
        },
        {
            "formatter": lambda view: "DNS View name '{}' with id {} is in state {}".format(view.display_name, view.id, view.lifecycle_state),
            "function_list"      : "list_views",
            "check2delete"       : lambda found: not found["is_protected"],
            "function_delete"    : "delete_view",
            "name_singular"      : "DNS view",
            "name_plural"        : "DNS views",
        },

        {
            "formatter"          : lambda zone: "DNS Zone {} name '{}' of type {}".format( zone.id, zone.name, zone.zone_type ),
            "function_list"      : "list_zones",
            # "function_delete"    : "delete_zone",
            "name_singular"      : "DNS Zone",
            "name_plural"        : "DNS Zones",
        },

        # {
        #     # "formatter"          : lambda instance: "XXX instance with OCID {} / name '{}' is in state {}".format( instance.id, instance.name, instance.lifecycle_state ),
        #     "function_list"      : "list_xxx",
        #     "kwargs_list"        : {
        #                            },
        #     # this isn't enough - we need to stop it AND wait for it to be stopped before we can delete it
        #     "function_predelete" : "stop_xxx",
        #     "function_delete"    : "delete_xxx",
        #     "name_singular"      : "XXX",
        #     "name_plural"        : "XXXXs",
        # },
    ]


    def list_objects(self, o, region, this_compartment, **kwargs):
        if o["name_plural"] == "DNS Resolver Endpoints":
            # DNS Resolver Endpoints
            endpoints = []
            logging.debug("Getting all resolvers in compartment {}".format(this_compartment))
            resolvers = oci.pagination.list_call_get_all_results( getattr((self.clients[region]), "list_resolvers"),this_compartment, **{}).data
            if len(resolvers):
                logging.debug("Found {} resolvers".format( len(resolvers) ))
                for resolver in resolvers:
                    # endpoints.extend( oci.pagination.list_call_get_all_results(getattr((self.clients[region]), "list_resolver_endpoints"),resolver.id,**{}).data )
                    en = oci.pagination.list_call_get_all_results(getattr((self.clients[region]), "list_resolver_endpoints"),resolver.id,**{}).data
                    # endpoints.extend(en)
                    # the result doesn't have the resolver ID
                    for e in en:
                        endpoints.append({
                            "name": e.name,
                            "endpoint_id": resolver.id
                        })

            return endpoints

        raise NotImplementedError

    def delete_object(self, object, region, found_object):
        if object["name_plural"] == "DNS Resolver Endpoints":
            # DNS Resolver Endpoints
            f = getattr((self.clients[region]), "delete_resolver_endpoint")
            f( found_object.endpoint_id, found_object.name )
            return

        raise NotImplementedError

    def check2delete(self,found):
        pass