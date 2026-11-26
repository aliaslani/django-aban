import logging
from time import perf_counter
from uuid import uuid4

logger = logging.getLogger("bazaarche.requests")


# class ExampleMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         response = self.get_response(request)
#
#         return response



class RequestIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.request_id = str(uuid4())
        response = self.get_response(request)
        response["X-Request-ID"] = request.request_id
        return response


class RequestTimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = perf_counter()
        response = self.get_response(request)
        elapsed = (perf_counter() - start) * 1000
        response["X-Request-Duration-ms"] = f"{elapsed:.2f}"
        logger.info(
            "request_id=%s method=%s status=%s duration_ms=%.2f",
            request.request_id,
            request.method,
            response.status_code,
            elapsed,
        )
        return response
