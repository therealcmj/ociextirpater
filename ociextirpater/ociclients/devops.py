import oci
from ociextirpater.OCIClient import OCIClient


class devops(OCIClient):
    service_name = "DevOps"
    clientClass = oci.devops.DevopsClient

    objects = [
        {
            "name_singular"      : "Project",
            "name_plural"        : "Projects",
            "formatter"          : lambda project: "Devops Project with OCID {} / name '{}' is in state {}".format(project.id, project.name, project.lifecycle_state),

            "function_list"      : "list_projects",
            "function_delete"    : "delete_project",
        },
    ]
