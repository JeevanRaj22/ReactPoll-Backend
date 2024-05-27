#from django.db.models.query import QuerySet
#from django.shortcuts import render,get_object_or_404
# from django.http import HttpResponse,HttpResponseRedirect
# from django.db.models import F
# from django.urls import reverse
# from django.views.generic import ListView,DetailView
from .models import Question,Choice,Tags
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from django.utils import timezone
import json


# Create your views here.
# def index(request):
#     questions = Question.objects.order_by("-pub_date")[:5]

#     return render(request,"polls/index.html",{ "question_list" : questions})

# def detail(request,question_id):
#     q = get_object_or_404(Question,pk=question_id)
#     return render(request,"polls/details.html",{ "question" : q })

# def results(request,question_id):
#     q = get_object_or_404(Question,pk=question_id)
#     return render(request,"polls/results.html",{ "question":q})

# class IndexView(ListView):
#     template_name = "polls/index.html"

#     def get_queryset(self):
#         return Question.objects.order_by("-pub_date")[:5]

# class DetailsView(DetailView):
#     model = Question
#     template_name = "polls/details.html"

# class ResultView(DetailView):
#     model = Question
#     template_name = "polls/results.html"
    

# def vote(request,question_id):
#     question = get_object_or_404(Question,pk=question_id)
#     try:
#         choice = question.choice_set.get(pk = request.POST["choice"])
#     except (KeyError,Choice.DoesNotExist):
#         return render(request,"polls/details.html",
#                       {"question" : question, "errormessage":"You didn't select a choice"})
#     choice.votes = F("votes")+1
#     choice.save()
#     return HttpResponseRedirect(reverse("polls:results",args=(question.id,)))

# from django.shortcuts import get_object_or_404
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Question,Choice
# from .serializers import QuestionSerializer,ChoiceSerializer
# 

@csrf_exempt
def index(request,id = None):
    if request.method == "GET":
        #get a poll
        if id is not None:
            data = dict()
            try:
                q = Question.objects.get(id = id)
                data["Question"] = q.question_text
                choice = dict()
                for c in q.choice_set.all():
                    choice[c.choice_text] = c.votes
                data["OptionVote"] = choice
                data["QuestionId"] = id
                tags = list()
                for tag in q.tags.all():
                    tags.append(tag.tag_text)
                data["Tags"] = tags
                res = {"msg" : "fetched polls successfull","data": data, "success" : True}                
            except Question.DoesNotExist:
                res = {"msg":f"Question with id {id} not found","success": False}
            
            return JsonResponse(res)
        
        #get polls using tags
        elif len(request.GET.dict()) != 0:
            tags = request.GET["tags"].split(",")
            print(tags)
            questions = Question.objects.filter(tags__tag_text__in = tags).distinct()
            data = list()
            for q in questions:
                question = dict()
                question["Question"] = q.question_text
                choice = dict()
                for c in q.choice_set.all():
                    choice[c.choice_text] = c.votes
                question["OptionVote"] = choice
                question["QuestionId"] = q.id
                tags = list()
                for tag in q.tags.all():
                    tags.append(tag.tag_text)
                question["Tags"] = tags
                data.append(question)
            res = {"msg" : "fetched polls successfull","data": data, "success" : True} 
            if len(data) == 0:
                res = {"msg":f"There are no Questions with tags {tags} are found","success": False}
            
            return JsonResponse(res)

        #get all polls
        data = list()
        questions = Question.objects.all()
        for q in questions:
            question = dict()
            question["Question"] = q.question_text
            choice = dict()
            for c in q.choice_set.all():
                choice[c.choice_text] = c.votes
            question["OptionVote"] = choice
            question["QuestionId"] = q.id
            tags = list()
            for tag in q.tags.all():
                tags.append(tag.tag_text)
            question["Tags"] = tags
            data.append(question)
        res = {"msg" : "fetched polls successfull","data": data, "success" : True}
        return JsonResponse(res,status=200)
        
    
    #create poll
    elif request.method == "POST":
        data = json.loads(request.body)
        q = Question(question_text = data["Question"],pub_date = timezone.localtime())
        q.save()
        for choice,vote in data["OptionVote"].items():
            q.choice_set.create(choice_text = choice,votes = vote)
        for tag in data["Tags"]:
            try:
                t = Tags.objects.get(tag_text = tag)
            except Tags.DoesNotExist:
                t = Tags.objects.create(tag_text = tag)
                t.save()
            q.tags.add(t)
        res = {"msg" : "Inserted poll successfull", "success" : True}
        return JsonResponse(res)
    
    #update poll
    elif request.method == "PUT":
        option = json.loads(request.body)
        try:
            question = Question.objects.get(id = id)
            choice = question.choice_set.get(choice_text = option["incrementOption"])
            choice.votes = F("votes")+1
            choice.save()
            res = {"msg" : "vote submitted successfully", "success" : True}
        except Choice.DoesNotExist:
            res = {"msg":f"There are no Choice {option['incrementOption']} for the question id {id} are found",
                   "success": False}
        except Question.DoesNotExist:
            res = {"msg":f"Question with id {id} not found","success": False}
        
        return JsonResponse(res)

def tags(request):
    tags = []
    for t in Tags.objects.all():
        tags.append(t.tag_text)
    res = {"msg" : "fetched tags successfull","data": tags, "success" : True}
    return JsonResponse(res)