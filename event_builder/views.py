import requests
from dal import autocomplete
from django.http import HttpResponse
from django.urls import reverse
from django.views import generic
from requests import Response
from starlette import status

from event_builder.models import Event


class EventTitleAutocomplete(autocomplete.Select2ListView):
    # model = Event

    def get_list(self):
        print(self.request)

        if self.q:
            print(self.q)

        type_a_head_url = "http://localhost:8001/v1/search/typeahead"
        response: Response = requests.post(
            url=type_a_head_url, json={"text": self.q, "epochs": 1, "maxLength": 30, "numResponses": 3, "quantile": 1}
        )
        if response.status_code != status.HTTP_200_OK:
            return []

        return response.json()["result"]


class EventTextAutocomplete(autocomplete.Select2ListView):
    # model = Event

    def get_list(self):
        print(self.request)

        if self.q:
            print(self.q)

        type_a_head_url = "http://localhost:8001/v1/search/typeahead"
        response: Response = requests.post(
            url=type_a_head_url, json={"text": self.q, "epochs": 5, "maxLength": 50, "numResponses": 5}
        )
        if response.status_code != status.HTTP_200_OK:
            return []

        return response.json()["result"]


class IndexView(generic.CreateView):
    model = Event
    fields = ["title", "text"]
    template_name = "event_builder/index.html"

    def get_success_url(self):
        return reverse("event_builder:index")
