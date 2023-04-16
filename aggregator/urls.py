from django.urls import path
from aggregator.views import (
     ArticleDetailView, ArticleList, ArticleListByAuthor, ArticleListByDate, ArticleListByDomain, HomePageView, api_overview, get_comment_rating_value,
     register_request, login_request, logout_request,
     search_article_by_author, search_article_by_category,
     search_article_by_date, set_rating_value, test_request
)

urlpatterns = [
     path('', HomePageView.as_view(), name='home'),
     path('api/', api_overview, name='api_list'),
     path('test', test_request, name='test'),
     path("register/", register_request, name="register"),
     path("login/", login_request, name="login"),
     path("logout/", logout_request, name="logout"),
     path('articles/', ArticleList.as_view(), name='article_list'),
     path('articles/domain/<slug:pk>', ArticleListByDomain.as_view(), name='article_list_by_domain'),
     path('articles/author/<slug:pk>', ArticleListByAuthor.as_view(), name='article_list_by_author'),
     path('articles/date/<str:date>', ArticleListByDate.as_view(), name='article_list_by_date'),
     path('article/<slug:pk>', ArticleDetailView.as_view(), name='article_view'),
     path('article/search/category', search_article_by_category, name='search_article_by_category'),
     path('article/search/author', search_article_by_author, name="search_article_by_author"),
     path('article/search/date', search_article_by_date, name="search_article_by_date"),
     path('comment/rating/<int:comment_id>/', get_comment_rating_value, name='get_comment_rating'),
     path('comment/rating/', set_rating_value, name='set_comment_rating'),
    

]
