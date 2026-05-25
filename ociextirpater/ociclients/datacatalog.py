import oci
from ociextirpater.OCIClient import OCIClient

class datacatalog( OCIClient ):
    service_name = "Data Catalog"
    clientClass = oci.data_catalog.DataCatalogClient

    objects = [
        {
            "name_singular"      : "Private Endpoint",
            "name_plural"        : "Private Endpoints",
            "function_list"      : "list_catalog_private_endpoints",
            "function_delete"    : "delete_catalog_private_endpoint",
        },

        {
            "name_singular"      : "Data Catalog",
            "name_plural"        : "Data Catalogs",
            "function_list"      : "list_catalogs",
            "function_delete"    : "delete_catalog",
            "kwargs_delete"      :  {
                                        "is_lock_override": True,
                                    }
        },

        {
            "name_singular"      : "Metastore",
            "name_plural"        : "Metastores",
            "function_list"      : "list_metastores",
            "function_delete"    : "delete_metastore",
            "kwargs_delete"      :  {
                                        "is_lock_override": True,
                                    }
        }
    ]

