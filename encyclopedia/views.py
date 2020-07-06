from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from markdown2 import Markdown
from . import util
import random
import re
markdowner = Markdown()


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})

def search(request):
    q = request.GET.get('q')
    entry = util.get_entry(q)
    if entry:
        return HttpResponseRedirect(reverse_lazy('load_page', args=[q]))
    all = util.list_entries()
    if any(q.upper() in s.upper() for s in all):
        return render(request, "encyclopedia/searchresults.html", {"entries": [s for s in all if q.upper() in s.upper()]})
    messages.error(request, f'No matching entries was found for {q} !')
    return HttpResponseRedirect("/")

def random_page(request):
    entries = util.list_entries()
    random_entry= random.randint(0, len(entries)-1)
    return HttpResponseRedirect(reverse_lazy('load_page', args=[entries[random_entry]]))

def create_page(request):
    if request.method == 'POST':
        title = request.POST.get('title').strip()
        entry = request.POST.get('body').strip()
        entries = util.list_entries()
        if title.lower() in (everyentry.lower() for everyentry in entries):
            messages.error(request, f'Another Entry with the name of {title} exist!')
            return render(request, 'encyclopedia/createpage.html', {'title': title, 'body': entry})
        else:
            entry = f'# {title}\n\n {entry}'
            util.save_entry(title, entry)
            return HttpResponseRedirect(reverse_lazy('load_page', args=[title]))
    return render(request, 'encyclopedia/createpage.html')

def edit_page(request, title):
    entry = util.get_entry(title)
    if entry:
        if request.method == 'POST':
            entry = request.POST.get('body').strip()
            if len(entry) > 10:
                util.save_entry(title, entry)
                return HttpResponseRedirect(reverse_lazy('load_page', args=[title]))
            else:
                messages.error(request, f'New Entry Don\'t have enough characters!')
        return render(request, 'encyclopedia/editpage.html', {'body': entry, 'title': title})
    raise Http404("Entry does not exist")

def load_page(request, title):
    entry = util.get_entry(title)
    if entry:
        # To convert Markdown to HTML
        body = markdowner.convert(entry)
        check = re.match(r'<h1>([^<>]*)</h1>', body)
        title = check.group(1) if check else ''
        return render(request, 'encyclopedia/edit.html', {'entry': body, 'title': title})
    raise Http404("Entry does not exist")