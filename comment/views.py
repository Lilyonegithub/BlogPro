from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import CommentForm
# Create your views here.


class CommentView(TemplateView):
    http_method_names = ['post']
    template_name = 'comment/result.html'

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        target = request.POST.get('target')

        if comment_form.is_valid():
            isinstance = comment_form.save(commit=False)
            isinstance.target = target
            isinstance.save()
            successd = True
            return redirect(target)
        else:
            successd = False

        context = {
            'succeed': successd,
            'form': comment_form,
            'target': target
        }
        return self.render_to_response(context)


