from app.utils import error_data_to_str


class ResponseStatusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_template_response(self, request, response):

        if getattr(response, 'data', None) is None:
            response.data = {}
        if 200 <= response.status_code < 300:
            response.data['status'] = 'ok'
        else:
            response.data = {'status': error_data_to_str(response.data)}
        return response
