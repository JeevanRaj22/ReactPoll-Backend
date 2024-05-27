from django.contrib import admin
from . import models
# Register your models here.

class MyAdminSite(admin.AdminSite):
    site_header = "Jeevan's site"
class ChoiceInline(admin.TabularInline):
    model = models.Choice
    extra = 3
class TagsInline(admin.TabularInline):
    model = models.Tags.question_set.through
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,{ "fields" : ["question_text"]}),
        ("Date Information",{ "fields" : ["pub_date"]})
    ]
    inlines = [ChoiceInline,TagsInline]
    list_display = ["question_text","pub_date","was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]

admin_site = MyAdminSite(name="myadmin")
admin_site.register(models.Question,QuestionAdmin)
admin_site.register(models.Tags)
