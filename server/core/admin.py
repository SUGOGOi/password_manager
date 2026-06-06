from django.contrib import admin
from unfold.admin import ModelAdmin
from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken

admin.site.unregister(SocialApp)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialToken)


@admin.register(SocialApp)
class SocialAppAdmin(ModelAdmin):
    pass


@admin.register(SocialAccount)
class SocialAccountAdmin(ModelAdmin):
    pass


@admin.register(SocialToken)
class SocialTokenAdmin(ModelAdmin):
    pass
