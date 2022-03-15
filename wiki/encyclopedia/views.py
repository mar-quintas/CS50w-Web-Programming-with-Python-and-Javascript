from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    entry = util.get_entry(title)
    if entry == None:
        return HttpResponse(f"404 - {title} - was not found")
    else:
        entry = markdown2.markdown(util.get_entry(title))
        return render(request, "encyclopedia/title.html", {
            "title": title,
            "entry": entry,
        })

# Use the search bar to find entries
def search(request):
    search = request.GET["q"]
    entry = util.get_entry(search)

    if entry == None:
        entries = util.list_entries()
        matches = []

        #Check for substrings
        for entry in entries:
            if search.lower() in entry.lower():
                matches.append(entry)

        if not matches:
            return HttpResponse(f"404 - {search} - was not found")
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": matches
            })
    else:
        return redirect(f'wiki/{search}')

# Add a new wiki entry
def new_entry(request):
    class NewEntryForm(forms.Form):
        entry_title = forms.CharField(label="Title")
        entry_content = forms.CharField(widget=forms.Textarea(attrs={'size':'40'}), label="Content")

    if request.method == "POST":
        form = NewEntryForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["entry_title"]
            content = form.cleaned_data['entry_content']
            entries = util.list_entries()

            for entry in entries:
                if title.lower() == entry.lower():
                    return HttpResponse(f"404 - {title} - entry already exists")

            util.save_entry(title, content)
            return redirect(f'wiki/{title}')

        else:
            return render(request, "encyclopedia/new_entry.html",{
            "form": form
            })

    return render(request, "encyclopedia/new_entry.html", {
    "form": NewEntryForm()
    })

# Edit a wiki entry
def edit(request, title):
    entry = util.get_entry(title)

    class EditEntryForm(forms.Form):
        entry_content = forms.CharField(widget=forms.Textarea(attrs={'size':'40'}), label="Content", initial=entry)

    if request.method == 'POST':
        form = EditEntryForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data['entry_content']
            util.save_entry(title, content)
            #the user will be redirected to the edited entry's page
            return redirect(f'/wiki/{title}')
        else:
            return render(request, "encyclopedia/edit.html",{
            "form": form
            })
    elif request.method == 'GET':
        return render(request, "encyclopedia/edit.html", {
        "form": EditEntryForm(),
        "title": title,
        })
    return HttpResponse(f"404 method not allowed")
