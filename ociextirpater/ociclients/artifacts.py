import logging

import oci
from ociextirpater.OCIClient import OCIClient

class artifacts( OCIClient ):
    service_name = "Artifacts"
    clientClass = oci.artifacts.ArtifactsClient
    # compositeClientClass = oci.artifacts.ArtifactsClientCompositeOperations

    objects = [
        {
            "name_singular"      : "Container Image",
            "name_plural"        : "Container Images",

            "function_list"      : "list_container_images",
            "function_delete"    : "delete_container_image",
        },

        {
            "name_singular"      : "Container Repository",
            "name_plural"        : "Container Repositories",

            "function_list"      : "list_container_repositories",
            "function_delete"    : "delete_container_repository",
        },

        {
            "name_singular"      : "Generic Repository",
            "name_plural"        : "Generic Repositories",

            "function_list"      : "list_repositories",
            "function_delete"    : "delete_repository",
        },

    ]


    def predelete(self,object,region,found_object):
        if object['name_singular'] == "Generic Repository":
            logging.info("Generic repository must be empty before it is removed. Please wait while I do that...")
            logging.debug("Getting a list of all artifacts in repository")
            kwargs = {}
            xs = oci.pagination.list_call_get_all_results(self.clients[region].list_generic_artifacts,
                                                          found_object.compartment_id,
                                                          found_object.id,
                                                          **kwargs).data

            i = 0
            for art in xs:
                logging.debug("Deleting {}".format(art.display_name))
                if art.lifecycle_state == 'AVAILABLE':
                    self.clients[region].delete_generic_artifact(art.id)
                    i = i + 1
                    if 0 == i % 100:
                        logging.info("Deleted {} artifacts from repository so far".format(i))

            logging.info("Deleted {} objects in total from generic artifact repository.".format(i))
# self.clients[region].list_generic_artifacts(found_object.compartment_id,found_object.id)
