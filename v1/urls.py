from django.urls import path

from v1.views.token import token_claim

urlpatterns = [path("auth/claim/", token_claim, name="token_claim")]
