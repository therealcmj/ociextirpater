import logging
import oci
from ociextirpater.OCIClient import OCIClient

class opensearchcluster( OCIClient ):
    service_name = "OpenSearch cluster"
    clientClass = oci.opensearch.opensearch_cluster_client.OpensearchClusterClient

    objects = [
        {
            "name_singular"      : "OpenSearch cluster",
            "name_plural"        : "OpenSearch clusters",
            "function_list"      : "list_opensearch_clusters",
            "function_delete"    : "delete_opensearch_cluster",
        },
    ]
