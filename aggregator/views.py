import traceback
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.views import generic
from aggregator.forms import CommentForm, NewUserForm
from aggregator.logic_alternative import parse_domain
from aggregator.models import Article, ArticleSeenRecord, Author, Category, CustomUser, Domain, Comment, Rating
from aggregator.tasks import parse_article_source
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

import logging
from django.contrib.auth import get_user_model

from aggregator.response_models import ResponseMessage, Status

User = get_user_model()
logger = logging.getLogger()

@api_view(['GET'])
def test_request(request):
    try:
        parse_article_source("aif.ru")
        # parse_article_in_domain.delay(name)
        # response = ResponseMessage(status=Status.OK, message=f'Parsing by {name} was successfully executed')
    except Exception as exc:
        logger.exception(traceback.format_exc())
        # response = ResponseMessage(status=Status.BAD_PARSER_NAME, message=f'Not existed parser name - {name}')
    # return Response(response.json())
    response = Response(status=Status.OK, data='Success!')
    return response

@api_view(['POST'])
def search_article_by_category(request):
    return Response(Article.objects.filter(category__pk__in=request.data['category_ids']).values())

@api_view(['POST'])
def search_article_by_author(request):
    return Response(Article.objects.filter(author__pk__in=request.data['author_ids']).values())

@api_view(['POST'])
def search_article_by_date(request):
    return Response(Article.objects.filter(date__range=[request.data['date_min'], request.data['date_max']]).values())



class HomePageView(generic.ListView):
    template_name = 'articles/home.html'
    model = Article 
    queryset = Article.objects.order_by('-date')[:6]

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        context["categories"] = Category.objects.all()
        return self.render_to_response(context)


class ArticleList(generic.ListView):
    template_name = 'articles/list.html'
    model = Article 
    paginate_by = 12
    queryset = Article.objects.order_by('-date')


class ArticleListByDomain(generic.ListView):
    template_name = 'articles/list_by_domain.html'
    model = Article 
    paginate_by = 12
    
    def get_queryset(self, **kwargs):
       return Article.objects.filter(domain=self.kwargs['pk'])
        
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        context["domain_obj"] = Domain.objects.get(id=self.kwargs['pk'])
        return self.render_to_response(context)


class ArticleListByAuthor(generic.ListView):
    template_name = 'articles/list_by_author.html'
    model = Article 
    paginate_by = 12
    
    def get_queryset(self, **kwargs):
       return Article.objects.filter(author=self.kwargs['pk'])
        
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        try:
            context["author_obj"] = Author.objects.get(id=self.kwargs['pk'])
        except Author.DoesNotExist:
             return HttpResponseNotFound("Such author not found")
        return self.render_to_response(context)
    

class ArticleListByDate(generic.ListView):
    template_name = 'articles/list_by_date.html'
    model = Article 
    paginate_by = 12
    
    def get_queryset(self, **kwargs):
       date = self.kwargs['date'].split('-')
       return Article.objects.filter(date__year=date[-1], date__month=date[1], date__day=date[0])
        
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        context["date"] = self.kwargs['date']
        return self.render_to_response(context)


class ArticleListByCategory(generic.ListView):
    template_name = 'articles/list_by_category.html'
    model = Article 
    paginate_by = 12
    
    def get_queryset(self, **kwargs):
       return Article.objects.filter(category__pk__in=[self.kwargs['pk'],])
        
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        try:
            context["category_obj"] = Category.objects.get(id=self.kwargs['pk'])    
        except Author.DoesNotExist:
             return HttpResponseNotFound("Such category not found")
        return self.render_to_response(context)


class ArticleDetailView(generic.DetailView):
    model = Article
    template_name = 'articles/view.html'

    def get_context_data(self , **kwargs):
        data = super().get_context_data(**kwargs)
        article = self.get_object()
        try:
            if not ArticleSeenRecord.objects.get(article=article, user=self.request.user):
                ArticleSeenRecord(user=self.request.user, article=article).save()
        except:
            ArticleSeenRecord(user=self.request.user, article=article).save()
        connected_comments = Comment.objects.filter(article=article)
        logger.warning(f'object - {article}')
        logger.warning(f'comments - {connected_comments}')
        number_of_comments = connected_comments.count() # 0 if connected_comments is None else len(connected_comments)
        data['comments'] = connected_comments
        data['no_of_comments'] = number_of_comments
        data['comment_form'] = CommentForm()
        data['no_of_seen'] = article.seen_by_article
        return data

    def post(self , request , *args , **kwargs):
        if self.request.user.is_anonymous:
            return redirect('login')
        comment_form = CommentForm(self.request.POST)
        if comment_form.is_valid():
            content = comment_form.cleaned_data['content']
            try:
                parent = comment_form.cleaned_data['parent']
            except:
                parent=None
        else:
            logger.warning(comment_form.errors.as_data())
        new_comment = Comment(content=content, user=CustomUser.objects.get(id=self.request.user.id), parent=parent, article=self.get_object())
        new_comment.save()
        return redirect(self.request.path_info)


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("home")
        else:
            logger.warning(form.errors.as_data())
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = NewUserForm()
    return render(request=request, template_name="users/register.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("home")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="users/login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("home")


@api_view(['POST'])
def set_rating_value(request):
    comment_id, comment_rating =  request.data['comment_id'], request.data['comment_rating']
    if request.user.is_anonymous:
        response = ResponseMessage(status=Status.USER_NOT_AUTHENTICATED, message='User not authenticated')
        return Response(response.json())
        
    comment = Comment.objects.get(pk=comment_id)
    response = ResponseMessage(status=Status.OK, message=f'Rating {comment_rating} was set for comment with id {comment_id}')
    try:
        rating = Rating.objects.get(user=request.user, comment=comment)
        logger.warning(f'comment_rating: {comment_rating}, rating.value: {rating.value}, {int(comment_rating)!=rating.value}')
        if int(comment_rating)!=rating.value:
            rating.value = comment_rating
            rating.save()
        else:
            response = ResponseMessage(status=Status.ALREADY_EXIST, message=f'Rating {comment_rating} already exist for comment with id {comment_id}')
    except Exception as exc:
        Rating(user=request.user, value=comment_rating, comment=comment).save()
    return Response(response.json())

@api_view(['GET'])
def get_comment_rating_value(request, comment_id):
    logger.info(request)
    try:
        comment = Comment.objects.get(pk=comment_id)
        response = ResponseMessage(status=Status.OK, message=str(comment.calculate_rating))
    except Exception as exc:
        response = ResponseMessage(status=Status.ERROR, message=str(exc))
         
    return Response(response.json())


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'url1': 'sadf',
        'url2': 'adxbwf'
    }
    return Response(api_urls)