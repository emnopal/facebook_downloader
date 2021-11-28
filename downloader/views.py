from django.shortcuts import render

from django.http import (
    Http404,
    HttpResponseRedirect
)

from .models import Parse

from django import forms


class ParseForm(forms.ModelForm):
    raw_url = forms.URLField(widget=forms.URLInput(
        attrs={
            "class": "form-control form-control-lg",
            "placeholder": "masukin link dimari",
            "style": "text-align: center;",
            "oninvalid": "this.setCustomValidity('masukin link dimari gan')",
            'oninput': "setCustomValidity('masukin link nya yang bener gan')"}
    ))

    class Meta:
        model = Parse
        fields = ('raw_url',)


def home(request):
    template = 'index.html'
    context = {}

    context['form'] = ParseForm()

    if request.method == 'GET':
        return render(request, template, context)

    elif request.method == 'POST':
        used_form = ParseForm(request.POST)

        # If URL is valid
        if used_form.is_valid():
            downloadable_object = used_form.save()
            context['downloadable_url'] = downloadable_object.downloadable_url
            context['raw_url'] = downloadable_object.raw_url
            context['social_media_source'] = downloadable_object.social_media_source
            return render(request, template, context)

        # Else
        context['errors'] = used_form.errors

        return render(request, template, context)


def downloadable_parse_url(request, downloadable_url):
    try:
        parsed_url = Parse.objects.get(downloadable_url=downloadable_url)
        parsed_url.times_followed += 1
        parsed_url.save()
        return HttpResponseRedirect(parsed_url.raw_url)
    except:
        raise Http404('This link is broken')
