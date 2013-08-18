from django.contrib import admin
from polls.models import Choice, Poll, Comment


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class EntryInline(admin.TabularInline):
    model = Comment
    extra = 3




