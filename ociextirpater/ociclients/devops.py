import oci
import logging
from ociextirpater.OCIClient import OCIClient

class devops(OCIClient):
    service_name = "DevOps"
    clientClass = oci.devops.DevopsClient
    compositeClientClass = oci.devops.devops_client_composite_operations.DevopsClientCompositeOperations

    _kwargs_delete = {
                        "wait_for_states": [
                            oci.devops.models.WorkRequest.STATUS_SUCCEEDED,
                            oci.devops.models.WorkRequest.STATUS_FAILED,
                            ]
                    }

    objects = [
        # {
        #     "name_singular"      : "Project",
        #     "name_plural"        : "Projects",
        #     "formatter"          : lambda project: "Devops Project with OCID {} / name '{}' is in state {}".format(project.id, project.name, project.lifecycle_state),

        #     "function_list"      : "list_projects",
        #     # "function_delete"    : "delete_project",
        #     # this requests the project be deleted, but that takes 72 hours
        #     "function_delete"    : "schedule_cascading_project_deletion",
        # }


        {
            "name_singular"      : "Build Pipeline Stage",
            "name_plural"        : "Build Pipeline Stages",

            "function_list"      : "list_build_pipeline_stages",
            "c_function_delete"  : "delete_build_pipeline_stage_and_wait_for_state",
            "kwargs_delete"      :  _kwargs_delete
        },

        {
            "name_singular"      : "Build Pipeline",
            "name_plural"        : "Build Pipelines",

            "function_list"      : "list_build_pipelines",
            "c_function_delete"  : "delete_build_pipeline_and_wait_for_state",
            "kwargs_delete"      :  _kwargs_delete
        },

        {
            "name_singular"      : "Deploy Pipeline Stage",
            "name_plural"        : "Deploy Pipeline Stages",

            "function_list"      : "list_deploy_stages",
            "c_function_delete"  : "delete_deploy_stage_and_wait_for_state",
            "kwargs_delete"      :  _kwargs_delete
        },

        {
            "name_singular"      : "Deploy Pipeline",
            "name_plural"        : "Deploy Pipelines",

            "function_list"      : "list_deploy_pipelines",
            "c_function_delete"  : "delete_deploy_pipeline_and_wait_for_state",
            "kwargs_delete"      :  _kwargs_delete
        },

        {
            "name_singular"      : "Deploy Artifact",
            "name_plural"        : "Deploy Artifacts",

            "function_list"      : "list_deploy_artifacts",
            "c_function_delete"  : "delete_deploy_artifact_and_wait_for_state",
            "kwargs_delete"      :  _kwargs_delete

        },


        {
            "name_singular"      : "Deploy Environment",
            "name_plural"        : "Deploy Environments",

            "function_list"      : "list_deploy_environments",
            "c_function_delete"  : "delete_deploy_environment_and_wait_for_state",

            "kwargs_delete"      :  _kwargs_delete
        },


        {
            "name_singular"      : "Trigger",
            "name_plural"        : "Triggers",

            "function_list"      : "list_triggers",
            "c_function_delete"  : "delete_trigger_and_wait_for_state",

            "kwargs_delete"      :  _kwargs_delete
        },

        {
            "name_singular"      : "Repository",
            "name_plural"        : "Repositories",

            "function_list"      : "list_repositories",
            "c_function_delete"  : "delete_repository_and_wait_for_state",

            "kwargs_delete"      :  _kwargs_delete
        },

        {
            "name_singular"      : "External connection",
            "name_plural"        : "External connections",

            "function_list"      : "list_connections",
            "c_function_delete"  : "delete_connection_and_wait_for_state",

            "kwargs_delete"      :  _kwargs_delete
        },


        {
            "name_singular"      : "Project",
            "name_plural"        : "Projects",

            "function_list"      : "list_projects",
            # you'll note all of the above use c_function_delete and wait for the object to be deleted
            # i don't do that for the project because it's slightly faster to move on to the next object (devops project or other) without waiting
            "function_delete"    : "delete_project",
        },
    ]


    def findAllInCompartment(self, region, o, this_compartment, **kwargs):
        
        if o["name_plural"] != "Project":
            return oci.pagination.list_call_get_all_results(
                getattr((self.clients[region]), o["function_list"]),
                **{"compartment_id":this_compartment}).data
    
        raise NotImplementedError

