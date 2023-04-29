from django.urls import path
from aggregator.views import (
     ArticleDetailView, ArticleList, ArticleListByAuthor, ArticleListByCategory, ArticleListByDate, ArticleListByDomain, HomePageView, get_comment_rating_value, get_data_for_user_profile, partial_search,
     register_request, login_request, logout_request,
     search_article_by_author, search_article_by_category,
     search_article_by_date, set_rating_value, test_request
)

urlpatterns = [
     path('', HomePageView.as_view(), name='home'),
     path('test', test_request, name='test'),
     path("register/", register_request, name="register"),
     path("login/", login_request, name="login"),
     path("logout/", logout_request, name="logout"),
     path("profile/", get_data_for_user_profile, name='user_profile'),
     path('partial-search/', partial_search, name='partial_search'),
     path('articles/', ArticleList.as_view(), name='article_list'),
     path('articles/category/<slug:pk>', ArticleListByCategory.as_view(), name='article_list_by_category'),
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
