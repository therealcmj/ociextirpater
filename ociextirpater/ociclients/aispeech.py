import oci
from ociextirpater.OCIClient import OCIClient

class aispeech( OCIClient ):
    service_name = "AI Speech"
    clientClass = oci.ai_speech.AIServiceSpeechClient

    objects = [
        {
            "name_singular"      : "Transcription Job",
            "name_plural"        : "Transcription Jobs",

            "function_list"      : "list_transcription_jobs",
            "function_delete"    : "delete_transcription_job",
        },

    ]


    def list_objects(self, o, region, this_compartment, **kwargs):
        if o["name_plural"] == "Transcription Jobs":
            return oci.pagination.list_call_get_all_results(
                getattr((self.clients[region]), "list_transcription_jobs"),
                **{"compartment_id":this_compartment}
            ).data
