from oci.circuit_breaker import CircuitBreakerStrategy
import logging

class MyCBS(CircuitBreakerStrategy):
    name = "Extirpater Circuit Breaker Strategy"

    class MyCBSException(Exception):
        pass

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def is_transient_error(self, status_code, service_code):
        if status_code == 401:
            logging.error("Got 401 - is identity replicated to this region?")
            raise self.MyCBSException("401 Server Error when making API call")

        if status_code == 500:
            logging.error("Got 500 error. Treating as failure (vs transient) and raising as exception.")
            raise self.MyCBSException("500 Server Error when making API call")
        return super().is_transient_error(status_code, service_code )
