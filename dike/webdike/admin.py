from django.contrib import admin

from webdike.models import *


def list_display_all(cls, blacklist=[]):
    l = [x.name for x in cls._meta.fields if x.name != 'id']
    for b in blacklist:
        l.remove(b)
    return l


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = list_display_all(UserProfile)


@admin.register(UserHistory)
class UserHistoryAdmin(admin.ModelAdmin):
    list_display = list_display_all(UserHistory)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['id'] + list_display_all(Document)


@admin.register(Sentence)
class SentenceAdmin(admin.ModelAdmin):
    list_display = list_display_all(Sentence)


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ['id'] + list_display_all(Step, ['result'])
    list_filter = ['stage', 'sentence']


@admin.register(StepLog)
class StepLogAdmin(admin.ModelAdmin):
    list_display = list_display_all(StepLog)


