
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .google_chart import google_graph

import json
from datetime import date

from .models import Choice, Question, DAU

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        Question.objects.filter(pub_date__lte=timezone.now()) returns a queryset containing
        Questions whose pub_date is less than or equal to - that is, earlier than or equal to - timezone.now.
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


pizza_col_def = [("Topping", "string"), ("Slices", "number")]

pizza_rows = [
    ("Mushrooms", 2),
    ("Onions", 3),
    ("Olives", 1),
    ("Zucchini", 2)
]

lifespan_col_def = [("Person", "string"), ("BornDate", "date")]

lifespan_rows = [
    ("Joe", date(2010, 10, 30)),
    ("Bob", date(2014, 11, 30)),
    ("Frank", date(2020, 9, 30)),
    ("Mark", date(2022, 7, 5))
]

# Example of input data...
dau_col_def = [("Date", "date"), ("Users",  "number")]

def my_json(request, question_id):
    json = "{}"

    if question_id == "1":
        header = {"title": "Pizza", "subtotal": str(len(pizza_rows)) + " pieces"}
        gtable = google_graph.GoogleGraph(header, pizza_col_def)
        for row in pizza_rows:
            gtable.add_row(row)
        json = gtable.to_json()

    if question_id == "2":
        latest_date = max([d[1] for d in lifespan_rows])
        header = {"title": "Lifespans", "subtotal": "latest: " + str(latest_date)}
        gtable = google_graph.GoogleGraph(header, lifespan_col_def)
        for row in lifespan_rows:
            gtable.add_row(row)
        json = gtable.to_json()

    if question_id == "3":
        qset = DAU.objects.all()
        avg = "No Users"
        if len(qset) > 0:
            avg = "Average: {0}".format(sum([q.active_users for q in qset]) / len(qset))
        header = {"title": "DAU", "subtotal": avg}
        gtable = google_graph.GoogleGraph(header, dau_col_def)
        for q in qset:
            row = (q.date, q.active_users)
            gtable.add_row(row)
        json = gtable.to_json()

    return HttpResponse(json, content_type='application/json')
