
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .google_chart import google_graph

import json
import collections

from .models import Choice, Question

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




def my_json(request, question_id):
    data = {'foo': 'bar', 'hello': 'world'}
    qset = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    qdict = {}
    i = 0
    for q in qset:
        qdict[i] = str(q)
        print(q)
        i += 1
    return HttpResponse(json.dumps(qdict), content_type='application/json')


# Example of input data...
col_def = [("Topping", "string"), ("Slices",  "number")]

my_rows = [
            ("Mushrooms", 2),
            ("Onions", 3),
            ("Olives", 5),
            ("Zucchini", 2)
         ]

def my_json(request, question_id):
    json = "{}"

    if question_id == "1":
        gtable = google_graph.GoogleGraph("Pizza Chart", col_def)
        for row in my_rows:
            gtable.add_row(row)
        json = gtable.to_json()


    if question_id == "2":
        gtable = google_graph.GoogleGraph("Crusty Chart", col_def)
        for row in my_rows:
            gtable.add_row(row)
        json = gtable.to_json()


    return HttpResponse(json, content_type='application/json')
