import logging
import oci
from ociextirpater.OCIClient import OCIClient

from oci.util import Sentinel

missing = Sentinel("Missing")
from oci import retry, circuit_breaker  # noqa: F401


class myIdentityClient(oci.identity.IdentityClient):
    def deactivate_domain(self, domain_id, **kwargs):
        import six
        # Required path and query arguments. These are in camelCase to replace values in service endpoints.
        required_arguments = ['domainId']
        resource_path = "/domains/{domainId}/actions/deactivate?isForceDeactivate=true"
        method = "POST"
        operation_name = "deactivate_domain"
        api_reference_link = "https://docs.oracle.com/iaas/api/#/en/identity/20160918/Domain/DeactivateDomain"

        # Don't accept unknown kwargs
        expected_kwargs = [
            "allow_control_chars",
            "retry_strategy",
            "opc_request_id",
            "opc_retry_token",
            "if_match"
        ]
        extra_kwargs = [_key for _key in six.iterkeys(kwargs) if _key not in expected_kwargs]
        if extra_kwargs:
            raise ValueError(
                f"deactivate_domain got unknown kwargs: {extra_kwargs!r}")

        path_params = {
            "domainId": domain_id
        }

        path_params = {k: v for (k, v) in six.iteritems(path_params) if v is not missing}

        for (k, v) in six.iteritems(path_params):
            if v is None or (isinstance(v, six.string_types) and len(v.strip()) == 0):
                raise ValueError(f'Parameter {k} cannot be None, whitespace or empty string')

        header_params = {
            "accept": "application/json",
            "content-type": "application/json",
            "opc-request-id": kwargs.get("opc_request_id", missing),
            "opc-retry-token": kwargs.get("opc_retry_token", missing),
            "if-match": kwargs.get("if_match", missing)
        }
        header_params = {k: v for (k, v) in six.iteritems(header_params) if v is not missing and v is not None}

        retry_strategy = self.base_client.get_preferred_retry_strategy(
            operation_retry_strategy=kwargs.get('retry_strategy'),
            client_retry_strategy=self.retry_strategy
        )
        if retry_strategy is None:
            retry_strategy = retry.DEFAULT_RETRY_STRATEGY

        if retry_strategy:
            if not isinstance(retry_strategy, retry.NoneRetryStrategy):
                self.base_client.add_opc_retry_token_if_needed(header_params)
                self.base_client.add_opc_client_retries_header(header_params)
                retry_strategy.add_circuit_breaker_callback(self.circuit_breaker_callback)
            return retry_strategy.make_retrying_call(
                self.base_client.call_api,
                resource_path=resource_path,
                method=method,
                path_params=path_params,
                header_params=header_params,
                allow_control_chars=kwargs.get('allow_control_chars'),
                operation_name=operation_name,
                api_reference_link=api_reference_link,
                required_arguments=required_arguments)
        else:
            return self.base_client.call_api(
                resource_path=resource_path,
                method=method,
                path_params=path_params,
                header_params=header_params,
                allow_control_chars=kwargs.get('allow_control_chars'),
                operation_name=operation_name,
                api_reference_link=api_reference_link,
                required_arguments=required_arguments)


class identitydomain( OCIClient ):
    service_name = "Identity Domain"
    clientClass = myIdentityClient

    # clientClass = oci.identity_domains.IdentityDomainsClient
    # compositeClientClass = oci.identity_domains.IdentityDomainsClientCompositeOperations


    objects = [
        {
            "name_singular"      : "Identity Domain",
            "name_plural"        : "Identity Domains",

            "function_list"      : "list_domains",
            "function_delete"    : "delete_domain",
        },

    ]

    # def __init__(self,config):
    #     super().__init__(config)


    def predelete(self,object,region,found_object):
        if object["name_plural"] == "Identity Domains":
            f = getattr((self.clients[region]), "deactivate_domain")
            logging.info("Attempting to deactivate domain")
            f(found_object.id)
            return

        raise NotImplementedError

    # def delete_object(self, object, region, found_object):
    #     if object["name_plural"] == "DNS Resolver Endpoints":
    #         # DNS Resolver Endpoints
    #         f = getattr((self.clients[region]), "delete_resolver_endpoint")
    #         logging.info( "Deleting {}".format(object["name_singular"]) )
    #         f( found_object["endpoint_id"], found_object["name"] )
    #         return
    #
    #     raise NotImplementedError
