import logging
import oci
from ociextirpater.OCIClient import OCIClient

class opensearchbackup( OCIClient ):
    service_name = "OpenSearch backup"
    clientClass = oci.opensearch.opensearch_cluster_backup_client.OpensearchClusterBackupClient

    objects = [
        {
            "name_singular"      : "OpenSearch cluster backup",
            "name_plural"        : "OpenSearch cluster backups",
            "function_list"      : "list_opensearch_cluster_backups",
            "function_delete"    : "delete_opensearch_cluster_backup",
        },
    ]
