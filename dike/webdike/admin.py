from django.contrib import admin

from webdike.models import *


def list_display_all(cls):
    return [x.name for x in cls._meta.fields if x.name != 'id']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = list_display_all(UserProfile)


@admin.register(UserHistory)
class UserHistoryAdmin(admin.ModelAdmin):
    list_display = list_display_all(UserHistory)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = list_display_all(Document)


@admin.register(Sentence)
class SentenceAdmin(admin.ModelAdmin):
    list_display = list_display_all(Sentence)


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = list_display_all(Step)


