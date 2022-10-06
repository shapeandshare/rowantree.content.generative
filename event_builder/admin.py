from django.contrib import admin

from event_builder.models import Event, EventForm

# class TitleInline(admin.TabularInline):
#     model = Event
#     form = EventForm
# admin.site.register(Event, EventAdmin)


class EventAdmin(admin.ModelAdmin):
    # list_display = ("title", "text")
    form = EventForm


admin.site.register(Event, EventAdmin)
