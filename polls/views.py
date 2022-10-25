import sqlite3
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Question, Choice
from django.contrib.auth.decorators import login_required

from django.urls import reverse
from django.views import generic

def vote(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html",{
            "question":question,
            "error_message":"You didn't select a choice.",
        }
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


def add_choice(request, question_id):

    connection=sqlite3.connect("db.sqlite3")
    add_choice = request.POST["add_choice"]
    connection.execute(f"INSERT INTO Polls_choice (choice_text, votes, question_id) values ('{add_choice}', 0, {question_id})")
    connection.commit()


    # question = get_object_or_404(Question,pk=question_id)
    # c = Choice(choice_text=request.POST["add_choice"], votes=0, question=question)
    # c.save()

    return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"