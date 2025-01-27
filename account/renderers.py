import json

from rest_framework.renderers import JSONRenderer


class AccountRenderer(JSONRenderer):
    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if "ErrorDetail" in str(data):
            return json.dumps({"errors": data})
        return json.dumps(data)
