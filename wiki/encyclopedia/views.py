from django.shortcuts import render
from django.http import HttpResponse
import markdown2


from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    entry = util.get_entry(title)
    if entry == None:
        # render search result
        # search substrings to lower de los dos lados.
        # entries_names = [CSS, Django]
        # find in entries_name [title]
        # each{ entries_name[i].lower == title.lower} => entries_name[i]
        # render list entries_names_search_result un subset de entries_names como te lo da util.py
        return HttpResponse(f"404 - {title} - was not found")
    else:
        entry = markdown2.markdown(util.get_entry(title))
        return render(request, "encyclopedia/title.html", {
            "title": title,
            "entry": entry,
        })
