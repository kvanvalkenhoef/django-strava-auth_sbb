from django.conf import settings
from django.contrib.auth import login, logout, authenticate as strava_authenticate
from stravauth.backend import StravaV3Backend
from django import http
from django.shortcuts import redirect
from django.views import generic


class StravaRedirect(generic.RedirectView):
    """
        Redirects to the Strava oauth page
    """
    def get_redirect_url(self, approval_prompt="auto", scope="read", *args, **kwargs):
        from stravauth.utils import get_stravauth_url
        # print(approval_prompt + '_stravauth')
        return get_stravauth_url(approval_prompt, scope)


class StravaAuth(generic.View):
    url = None # Or default?
    
    def get(self, request, *args, **kwargs):
        code = request.GET.get("code", None)

        if not code:
            # Redirect to the strava url
            # print('Redirect to the strava url')
            view = StravaRedirect.as_view()
            return view(request, *args, **kwargs)

        # Log the user in
        user = strava_authenticate(code=code)
        # user = StravaV3Backend.authenticate(self, code=code)
        login(request, user)
        print(user,request)
        return http.HttpResponseRedirect(self.url)
        
    
class StravaUnAuth(generic.View):
    url = None  # Or default?

    def get(self, request, *args, **kwargs):
        # print(request.user.is_authenticated)
        logout(request)
        # Redirect to a success page.
        return http.HttpResponseRedirect(self.url)


    
    