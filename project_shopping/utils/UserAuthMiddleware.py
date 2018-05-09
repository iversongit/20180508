import datetime

import pytz
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

from shopper.models import UserSession


class AuthMiddleware(MiddlewareMixin):
    def process_request(self,request):
        # if request.path == '/shopapp/login/' or request.path == '/shopapp/regist/':
        #     return None
        ticket = request.COOKIES.get("ticket")
        # request.user = None
        if not ticket:
            return None
        #     return HttpResponseRedirect('/shopapp/login/')
        sessions = UserSession.objects.filter(session_data=ticket)
        if sessions:
            if datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC')) < sessions[0].expire_time:
                # 没有过期
                request.user = sessions[0].u
                # return None
            else:
                # 过期了
                sessions[0].delete()
        # return HttpResponseRedirect('/shopapp/login/')
