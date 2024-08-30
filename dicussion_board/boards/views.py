from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import *
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView, CreateView, DetailView, ListView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.
# =================================================================
# def home(request):
#     # boards = Board.objects.all()
#     # boards_names = []
#     # for board in boards:
#     #     boards_names.append(board.name)
#     #
#     # print(boards_names)
#     # return HttpResponse("hello, my name is mazen, this is my first web site!")
#     #
#     # response_html = "<br>".join(boards_names)
#     # return HttpResponse(response_html)
#     #
#     boards = Board.objects.all()
#     context = {}
#     context["boards"] = boards
#     return render(request, "boards/home.html", context)


class BoardListView(ListView):
    model = Board
    context_object_name = "boards"
    template_name = "boards/home.html"


def board_topics(request, id):
    # board = get_object_or_404(Board, id=id)
    context = {}
    try:
        board = get_object_or_404(Board, pk=id)
        # topics = board.topics.order_by("-created_dt").annotate(comments=Count("posts"))
        queryset = board.topics.order_by("-created_dt").annotate(
            comments=Count("posts")
        )
        page = request.GET.get("page", 1)
        paginator = Paginator(queryset, 20)
        topics = paginator.page(page)
        context["board"] = board
        context["topics"] = topics

    except Board.DoesNotExist:
        context["id"] = id
        return render(request, "boards/error.html", context)
    except PageNotAnInteger:
        topics = paginator.page(1)
        context["topics"] = topics
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
        context["topics"] = topics

    return render(request, "boards/topics.html", context)


@login_required
def new_topic(request, id):
    context = {}
    try:
        board = get_object_or_404(Board, pk=id)
        context["board"] = board
        # user = User.objects.first()  # user

        if request.method == "POST":
            form = NewTopicForm(request.POST)
            if form.is_valid():
                topic = form.save(commit=False)
                topic.board = board
                topic.created_by = request.user
                topic.save()
                post = Post.objects.create(
                    message=form.cleaned_data["message"],
                    created_by=request.user,
                    topic=topic,
                )
                return redirect("board_topics", id=board.pk)
            else:
                context["form"] = form
        else:
            form = NewTopicForm()
            context["form"] = form
    except Board.DoesNotExist:
        context["id"] = id
        return render(request, "boards/error.html", context)

    return render(request, "boards/new_topic.html", context)


def topic_posts(request, id, topic_id):
    context = {}
    topic = get_object_or_404(Topic, board__pk=id, pk=topic_id)

    session_key = "view_topic_{}".format(topic.pk)
    if not request.session.get(session_key, False):
        topic.views += 1
        topic.save()
        # request.session.set(session_key, True)
        request.session[session_key] = True

    context["topic"] = topic
    return render(request, "boards/topic_posts.html", context)


@login_required
def reply_topic(request, id, topic_id):
    context = {}
    try:
        topic = get_object_or_404(Topic, board__pk=id, pk=topic_id)
        context["topic"] = topic

        if request.method == "POST":
            form = PostForm(request.POST)  # forms
            if form.is_valid():
                post = form.save(commit=False)
                post.topic = topic

                post.created_by = request.user
                post.save()
                # context["form"] = form
                topic.updated_by = request.user
                topic.updated_dt = timezone.now()
                topic.save()

                # return redirect("topic_posts", id=board.id, topic_id=topic.pk)
                return redirect("topic_posts", id=id, topic_id=topic.pk)
            else:
                context["form"] = form
        else:
            form = PostForm()
            context["form"] = form
    except Board.DoesNotExist:
        context["id"] = id
        return render(request, "boards/error.html", context)

    return render(request, "boards/reply_topic.html", context)


@method_decorator(login_required, name="dispatch")
class PostUpdateView(UpdateView):
    model = Post
    fields = ("message",)
    template_name = "boards/edit_post.html"
    pk_url_kwarg = "post_id"
    context_object_name = "post"

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_dt = timezone.now()
        post.save()
        return redirect("topic_posts", id=post.topic.board.pk, topic_id=post.topic.pk)


def about(request):
    return HttpResponse(request, "yes")
