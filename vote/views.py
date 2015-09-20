from django.views.generic import View
from django.shortcuts import render_to_response

from models import Production

class VoteList(View):
    def get(self, *arg, **kwargs):
        productions = Production.objects.all()
        print productions
        print productions[0].get_all_image_url()
        return render_to_response('vote_list.html', {
                'productions': productions,
            })
