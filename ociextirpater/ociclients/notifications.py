import oci
from ociextirpater.OCIClient import OCIClient

class notifications( OCIClient ):
    service_name = "Notifications"
    clientClass = oci.ons.NotificationControlPlaneClient

    objects = [
        {
            "name_singular"      : "Topic",
            "name_plural"        : "Topics",

            "function_list"      : "list_topics",
            "formatter"          : lambda topic: "Notifications topic with OCID {} / description '{}' is in state {}".format(topic.topic_id, topic.description, topic.lifecycle_state),
            "function_delete"    : "delete_topic",
        },
    ]

    def predelete(self,object,region,found_object):
        # this copies the topic_id from the object into "id" because the code in OCIClient.py is expecting
        # to find "id" in the object and just passed that to the function_delete() function
        # so this is a cheap and easy workaround
        found_object.id = found_object.topic_id