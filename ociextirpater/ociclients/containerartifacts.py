import oci
from ociextirpater.OCIClient import OCIClient

class containerartifacts( OCIClient ):
    service_name = "Container Artifacts"
    clientClass = oci.artifacts.ArtifactsClient

    objects = [
        {
            "name_singular"      : "Container Repo",
            "name_plural"        : "Container Repos",

            "function_list"      : "list_container_repositories",
            # "formatter"          : lambda instance: "XXX instance with OCID {} / name '{}' is in state {}".format( instance.id, instance.name, instance.lifecycle_state ),
            "function_delete"    : "delete_container_repository",
        },

        # {
        #     "name_singular"      : "XXX",
        #     "name_plural"        : "XXXXs",

        #     "function_list"      : "list_xxx",
        #     "kwargs_list"        : {
        #                            },
        #     "formatter"          : lambda instance: "XXX instance with OCID {} / name '{}' is in state {}".format( instance.id, instance.name, instance.lifecycle_state ),
        #     "function_delete"    : "delete_xxx",
        # },
    ]
