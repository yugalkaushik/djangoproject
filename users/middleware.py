class BasicRequestLoggerMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(f" Request coming in: {request.method} {request.path}")
        
        response = self.get_response(request)
        
        print(f" Response going out: {response.status_code} for {request.path}")
        
        return response