from django.urls import path

from v1.views import info
from v1.views.curriculum import curriculum, curriculum_terms, curriculum_weeks
from v1.views.results import results, results_klasses, results_terms
from v1.views.token import token_claim

urlpatterns = [
    path("auth/claim/", token_claim, name="token_claim"),
    # info
    path("info/", info, name="info"),
    # curriculum views
    path("curriculum/", curriculum, name="curriculum"),
    path("curriculum/terms/", curriculum_terms, name="curriculum_terms"),
    path("curriculum/weeks/", curriculum_weeks, name="curriculum_weeks"),
    # results views
    path("results/", results, name="results"),
    path("results/terms/", results_terms, name="results_terms"),
    path("results/class/", results_klasses, name="results_klasses"),
]
