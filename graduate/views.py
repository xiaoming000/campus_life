from django.shortcuts import render
from .models import Graduate
from django.views.generic import ListView, DetailView


class GraduateView(ListView):
    model = Graduate
    template_name = 'graduate/graduate.html'
    context_object_name = 'graduate_list'

    def get_context_data(self, **kwargs):
        context = super(GraduateView, self).get_context_data(**kwargs)
        context.update({
            'nav': 5,
            'htitle': "毕业校友"
        })
        return context

