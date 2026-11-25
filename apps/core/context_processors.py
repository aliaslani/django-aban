def global_context(request):
    return {
        "app_name": "bazaarche", 
        "request_id": getattr(request, "request_id", "")
        }
