from django.urls import path
from aggregator.views import (
    ArticleDetailView, HomePageView, api_overview, parse,
    register_request, login_request, logout_request,
    search_article_by_author, search_article_by_category,
    search_article_by_date, set_rating_value
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('api/', api_overview, name='api_list'),
    path('parse/<str:name>', parse, name='parse'),
    path("register/", register_request, name="register"),
    path("login/", login_request, name="login"),
    path("logout/", logout_request, name="logout"),
    path('article/<slug:pk>', ArticleDetailView.as_view(), name='article_view'),
    path('article/search/category', search_article_by_category,
         name='search_article_by_category'),
    path('article/search/author', search_article_by_author,
         name="search_article_by_author"),
    path('article/search/date', search_article_by_date,
         name="search_article_by_date"),
    path('comment/rating/', set_rating_value, name='set_comment_rating')

]
