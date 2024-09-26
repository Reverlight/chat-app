from django.contrib import admin

from chat.models import Message, Thread


class ThreadAdmin(admin.ModelAdmin):
    list_display = ('pk', 'created', 'updated')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'sender', 'text', 'created', 'is_read', 'thread')


admin.site.register(Thread, ThreadAdmin)
admin.site.register(Message, MessageAdmin)
