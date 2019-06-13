from django.urls import path

from v1.views.curriculum import curriculum, curriculum_terms, curriculum_weeks
from v1.views.token import token_claim

urlpatterns = [
    path("auth/claim/", token_claim, name="token_claim"),
    # curriculum views
    path("curriculum/", curriculum, name="curriculum"),
    path("curriculum/terms/", curriculum_terms, name="curriculum_terms"),
    path("curriculum/weeks/", curriculum_weeks, name="curriculum_weeks"),
]
