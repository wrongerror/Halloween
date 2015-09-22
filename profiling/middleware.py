# -*- coding: UTF-8 -*-
from django.http import HttpResponse
import re

Redirect_USER_AGENTS = (re.compile(r'micromessenger', re.IGNORECASE), )
class RedirectMiddleware(object):
    def process_request(self, request):
        if 'HTTP_USER_AGENT' in request.META:
            for user_agent_regex in Redirect_USER_AGENTS:
                if not user_agent_regex.search(request.META['HTTP_USER_AGENT']):
                    return HttpResponse(
                        '<body style="margin-left:25%;margin-right:25%;marigin-top:80px;text-align: center; ">\
                        <div >\
                        <h2>请在微信中打开 :)</h2>\
                        </div>\
                        </body>\
                        ', 
                        content_type='text/html; charset=utf-8')
