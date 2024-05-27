from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
    # path("",views.IndexView.as_view(),name="index"),
    # path("<int:pk>",views.DetailsView.as_view(),name="details"),
    # path("<int:pk>/result",views.ResultView.as_view(),name="results"),
    # path("<int:question_id>/vote",views.vote,name="vote")
    path("",views.index,name = "index"),
    path("<int:id>",views.index,name = "index"),
    path("tags",views.tags,name = "tags")

]