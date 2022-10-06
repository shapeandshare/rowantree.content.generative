from dal import autocomplete
from django.urls import path, re_path

from .models import Event
from .views import EventTextAutocomplete, EventTitleAutocomplete, IndexView

# app_name = "event_builder"
urlpatterns = [
    # path("", views.index, name="index"),
    # path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # path("<int:question_id>/vote/", views.vote, name="vote"),
    path(
        "event-title-autocomplete/",
        EventTitleAutocomplete.as_view(),
        name="event-title-autocomplete",
    ),
    path(
        "event-text-autocomplete/",
        EventTextAutocomplete.as_view(),
        name="event-text-autocomplete",
    ),
    path("", IndexView.as_view(), name="index"),
]

# import djhacker
# from django import forms
# djhacker.formfield(
#     Event,
#     forms.ModelChoiceField,
#     widget=autocomplete.ListSelect2(url='event-title-autocomplete')
# )
