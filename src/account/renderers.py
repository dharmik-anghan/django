import json
from rest_framework import renderers

class UserRenderer(renderers.JSONRenderer):
    charset = 'utf-8'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        responce = ''
        if 'ErrorDetail' in str(data):
            responce = json.dumps({"errors": data})
        else:
            responce = json.dumps(data)
        return responce