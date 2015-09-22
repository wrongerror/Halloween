from django.views.generic import View
from django.shortcuts import render_to_response

from models import Production

class VoteList(View):
    def get(self, *arg, **kwargs):
        productions = Production.objects.all()
        return render_to_response('vote_list.html', {
                'productions': productions,
            })

from django.http import HttpResponse
class ProductionVote(View):
    def get(self, request, pk, *arg, **kwargs):
        try:
            production = Production.objects.get(pk=pk)
            count = production.vote()
            return HttpResponse(count)
        except:
            return HttpResponse(False)