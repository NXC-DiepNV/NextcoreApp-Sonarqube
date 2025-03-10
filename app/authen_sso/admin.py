from django.urls import path
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.contrib.auth import login, get_user_model
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from unfold.sites import UnfoldAdminSite
from decouple import config

from .models import LarkProfile
from .constants import LARK_LOGIN_CALLBACK_URI
from .services import exchange_code_for_user_info, lark_get_lark_login_url


class SSOAdminSite(UnfoldAdminSite):
    def login(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['lark_login_url'] = lark_get_lark_login_url()
        return super().login(request, extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(LARK_LOGIN_CALLBACK_URI,
                 self.lark_login_callback, name='lark_callback'),
        ]
        return custom_urls + urls

    @staticmethod
    def lark_login_callback(request):
        code = request.GET.get('code')
        if not code:
            # TODO handle render
            return render(request, 'admin/login_failed.html', {'error': _('Invalid callback from Lark')})

        # Gọi service xử lý logic
        user_data = exchange_code_for_user_info(code)

        if not user_data:
            # TODO handle render
            return render(request, 'admin/login_failed.html', {'error': _('Failed to authenticate with Lark')})

        user_name: str = user_data.get('user_id').lower()

        # Don't use class User 'cause it's not the custom user model
        User = get_user_model()

        user = User.objects.filter(username=user_name).first()

        if not user:
            first_name = user_data.get('name').split(' ')[0]
            last_name = user_data.get('name').split(' ')[1]
            try:
                with transaction.atomic():  # Start a transaction
                    # Create the user
                    user = User.objects.create_user(
                        email=user_data.get('email', ''),
                        business_email=user_name +
                        '@' + config('EMAIL_DOMAIN'),
                        username=user_name,
                        password=config('PASSWORD_DEFAULT'),
                        is_staff=True,  # Set user can login
                        is_superuser=False,  # Can access to model
                        first_name=first_name,
                        last_name=last_name,
                    )
                    user.save()

                    # Create the LarkProfile for the user
                    LarkProfile.objects.create(
                        user=user,
                        avatar_url=user_data.get('avatar_url', ''),
                        open_id=user_data.get('open_id', ''),
                        access_token=user_data.get('access_token', ''),
                    )

                # Log the user in and redirect if everything succeeds
                login(request, user)
                return redirect('/')

            except Exception as e:
                # Handle the error (e.g., log it, show an error message)
                print(f"Error during user/profile creation: {e}")
                return render(request, 'admin/login_failed.html', {'error': _('An error occurred during account creation.')})

        if user.is_staff:
            login(request, user)
            return redirect('/')

        return HttpResponseForbidden(_("You are not authorized to access the admin."))


sso_admin_site = SSOAdminSite()
