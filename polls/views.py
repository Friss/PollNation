# Create your views here.
import re

from operator import attrgetter
from itertools import chain

from django.utils import timezone
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth import login, authenticate, logout
from django.db.models import Sum
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms.formsets import formset_factory, BaseFormSet

from polls.models import Choice, Poll
from polls.forms import AuthenticateForm, UserCreateForm, CommentForm, PollForm, ChoiceForm


def IndexView(request):
    poll_list = Poll.objects.annotate(num_votes=Sum('choice__votes')).filter(pub_date__lte=timezone.now()).order_by(
        '-pub_date')
    paginator = Paginator(poll_list, 5) # Show 5 polls per page

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        polls = paginator.page(page)
    except (EmptyPage, InvalidPage):
        polls = paginator.page(paginator.num_pages)

    if request.user.is_authenticated():
        auth_form = False
        logged_in = True

    else:
        logged_in = False
        auth_form = AuthenticateForm()

    top_polls = Poll.objects.annotate(num_votes=Sum('choice__votes')).order_by('-num_votes')
    top_tags = Poll.tags.most_common()[:10]

    return render_to_response('polls/index.html',
                              {"polls": polls, "top_polls": top_polls, "top_tags": top_tags, "auth_form": auth_form,
                               "logged_in": logged_in}, context_instance=RequestContext(request))


def DetailsView(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    top_polls = Poll.objects.annotate(num_votes=Sum('choice__votes')).order_by('-num_votes')
    top_tags = Poll.tags.most_common()[:10]
    similar_polls = poll.tags.similar_objects()[:5]
    comment_form = CommentForm()
    if request.user.is_authenticated():
        auth_form = False
        logged_in = True

    else:
        logged_in = False
        auth_form = AuthenticateForm()
    return render_to_response('polls/detail.html',
                              {"poll": poll, "top_polls": top_polls, "top_tags": top_tags, "auth_form": auth_form,
                               "logged_in": logged_in, "comment_form": comment_form, "similar_polls": similar_polls},
                              context_instance=RequestContext(request))


def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        top_polls = Poll.objects.annotate(num_votes=Sum('choice__votes')).order_by('-num_votes')
        top_tags = Poll.tags.most_common()[:10]
        if request.user.is_authenticated():
            auth_form = False
            logged_in = True

        else:
            logged_in = False
            auth_form = AuthenticateForm()
        return render(request, 'polls/detail.html',
                      {'poll': p, 'error_message': "You didn't select a choice.", "top_polls": top_polls,
                       "top_tags": top_tags, "auth_form": auth_form,
                       "logged_in": logged_in}, context_instance=RequestContext(request))
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:detail', args=(p.id,)))


def login_view(request):
    if request.method == 'POST':
        form = AuthenticateForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            # Success
            return redirect('/polls')
        else:
            # Failure
            return IndexView(request)
    return redirect('/polls')


def logout_view(request):
    logout(request)
    return redirect('/polls')


def signup(request):
    user_form = UserCreateForm(data=request.POST)
    if request.method == 'POST':
        if user_form.is_valid():
            username = user_form.clean_username()
            password = user_form.clean_password2()
            user_form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/polls')
        else:
            return register(request, user_form=user_form)
    return redirect('/polls/register')



def comment(request):
    user_comment = CommentForm(data=request.POST)
    if request.method == 'POST':
        if user_comment.is_valid():
            comment = user_comment.save(commit=False)
            comment.user = request.user
            poll = Poll.objects.get(pk=request.POST['pollid'])
            comment.poll = poll
            comment.save()
            return DetailsView(request,request.POST['pollid'])
        else:
            return DetailsView(request,request.POST['pollid'])
    return redirect(request.path)


def register(request, user_form="none"):
    if user_form == "none":
        user_form = UserCreateForm()

    return render(request, 'polls/register.html', {
        'user_form': user_form,
    })


def directory(request):
    top_polls = Poll.objects.annotate(num_votes=Sum('choice__votes')).order_by('-num_votes')
    top_tags = Poll.tags.most_common()[:10]
    all_tags = Poll.tags.most_common()
    if request.user.is_authenticated():
        auth_form = False
        logged_in = True

    else:
        logged_in = False
        auth_form = AuthenticateForm()
    return render_to_response('polls/directory.html',
                              {"top_polls": top_polls, "top_tags": top_tags, "auth_form": auth_form,
                               "logged_in": logged_in, "all_tags": all_tags}, context_instance=RequestContext(request))


def search(request):
    query_string = ''
    found_entries = None
    
    top_polls = Poll.objects.annotate(num_votes=Sum('choice__votes')).order_by('-num_votes')
    top_tags = Poll.tags.most_common()[:10]
    
    if request.user.is_authenticated():
            auth_form = False
            logged_in = True

    else:
        logged_in = False
        auth_form = AuthenticateForm()

    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string, ['question'])

        tag_query = normalize_query(query_string)
        found_entries = Poll.objects.annotate(num_votes=Sum('choice__votes')).filter(entry_query).order_by('-pub_date').distinct()
        tag_entries = Poll.objects.filter(tags__name__in=tag_query).distinct()

        
        result_list = found_entries | tag_entries

        paginator = Paginator(result_list, 5) # Show 5 polls per page

        # Make sure page request is an int. If not, deliver first page.
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1

        # If page request (9999) is out of range, deliver last page of results.
        try:
            polls = paginator.page(page)
        except (EmptyPage, InvalidPage):
            polls = paginator.page(paginator.num_pages)

        

        

        return render_to_response('polls/search_results.html',
                                  {"top_polls": top_polls, "top_tags": top_tags, "auth_form": auth_form, "polls": polls,
                                   "logged_in": logged_in, 'query_string': query_string, 'result_list': result_list},
                                  context_instance=RequestContext(request))
    else:
        result_list = False
        return render_to_response('polls/search_results.html',
                              {"top_polls": top_polls, "top_tags": top_tags, "auth_form": auth_form,
                               "logged_in": logged_in, 'query_string': query_string, 'result_list': result_list},
                              context_instance=RequestContext(request))


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query | or_query
    return query

def create(request):
    
    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False

    ChoiceFormSet = formset_factory(ChoiceForm, max_num=10, formset=RequiredFormSet)
    if request.method == 'POST': # If the form has been submitted...
        poll_form = PollForm(request.POST) # A form bound to the POST data
        # Create a formset from the submitted data
        choice_formset = ChoiceFormSet(request.POST, request.FILES)

        if poll_form.is_valid() and choice_formset.is_valid():
            poll = poll_form.save(commit=False)
            if request.user.is_authenticated():
                poll.creator = request.user
            poll.save()
            poll_form.save_m2m()
            for form in choice_formset.forms:
                choice = form.save(commit=False)
                choice.poll = poll
                choice.save()
            top_polls = Poll.objects.annotate(num_votes=Sum('choice__votes')).order_by('-num_votes')
            top_tags = Poll.tags.most_common()[:10]
            all_tags = Poll.tags.most_common()
            if request.user.is_authenticated():
                auth_form = False
                logged_in = True

            else:
                logged_in = False
                auth_form = AuthenticateForm()
            return render_to_response('polls/detail.html',
                              {"poll": poll, "top_polls": top_polls, "top_tags": top_tags, "auth_form": auth_form,
                               "logged_in": logged_in, "all_tags": all_tags}, context_instance=RequestContext(request))
    else:
        poll_form = PollForm()
        choice_formset = ChoiceFormSet()



    top_polls = Poll.objects.annotate(num_votes=Sum('choice__votes')).order_by('-num_votes')
    top_tags = Poll.tags.most_common()[:10]
    all_tags = Poll.tags.most_common()
    if request.user.is_authenticated():
        auth_form = False
        logged_in = True

    else:
        logged_in = False
        auth_form = AuthenticateForm()
    return render_to_response('polls/create.html',
                              {"top_polls": top_polls, "top_tags": top_tags, "auth_form": auth_form,
                               "logged_in": logged_in, "all_tags": all_tags, "poll_form": poll_form, "choice_formset": choice_formset}, context_instance=RequestContext(request))


def account(request):
    if request.user.is_authenticated():
        poll_list = Poll.objects.annotate(num_votes=Sum('choice__votes')).filter(creator=request.user).order_by(
            '-pub_date')
        paginator = Paginator(poll_list, 5) # Show 5 polls per page

        # Make sure page request is an int. If not, deliver first page.
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1

        # If page request (9999) is out of range, deliver last page of results.
        try:
            polls = paginator.page(page)
        except (EmptyPage, InvalidPage):
            polls = paginator.page(paginator.num_pages)

        if request.user.is_authenticated():
            auth_form = False
            logged_in = True

        else:
            logged_in = False
            auth_form = AuthenticateForm()

        top_polls = Poll.objects.annotate(num_votes=Sum('choice__votes')).order_by('-num_votes')
        top_tags = Poll.tags.most_common()[:10]

        return render_to_response('polls/account.html',
                                  {"polls": polls, "top_polls": top_polls, "top_tags": top_tags, "auth_form": auth_form,
                                   "logged_in": logged_in}, context_instance=RequestContext(request))
    else:
       return redirect('/polls')

def delete(request, poll_id):
    if request.user.is_authenticated():
        poll = Poll.objects.get(pk=poll_id)

        auth_form = False
        logged_in = True
        top_polls = Poll.objects.annotate(num_votes=Sum('choice__votes')).order_by('-num_votes')
        top_tags = Poll.tags.most_common()[:10]


        if request.method == 'POST':
            poll = Poll.objects.get(pk=request.POST['id'])
            poll.delete()
            poll_list = Poll.objects.annotate(num_votes=Sum('choice__votes')).filter(creator=request.user).order_by(
            '-pub_date')
            paginator = Paginator(poll_list, 5) # Show 5 polls per page

            # Make sure page request is an int. If not, deliver first page.
            try:
                page = int(request.GET.get('page', '1'))
            except ValueError:
                page = 1

            # If page request (9999) is out of range, deliver last page of results.
            try:
                polls = paginator.page(page)
            except (EmptyPage, InvalidPage):
                polls = paginator.page(paginator.num_pages)

            return render_to_response('polls/account.html',
                                  {"polls": polls, "top_polls": top_polls, "top_tags": top_tags, "auth_form": auth_form,
                                   "logged_in": logged_in}, context_instance=RequestContext(request))
        else:

            return render_to_response('polls/delete.html',
                                  {"poll": poll, "top_polls": top_polls, "top_tags": top_tags, "auth_form": auth_form,
                                   "logged_in": logged_in}, context_instance=RequestContext(request))
    else:
        redirect('/polls/')