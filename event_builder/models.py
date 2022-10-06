from dal import autocomplete
from django import forms
from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=200)


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        widgets = {
            "title": autocomplete.ListSelect2(url="event-title-autocomplete"),
            "text": autocomplete.ListSelect2(url="event-text-autocomplete"),
        }
