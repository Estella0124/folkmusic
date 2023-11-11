from django.urls import path
from . import views

urlpatterns=[

    path('api/music_detail', views.search_by_id),
    path('api/search/tag', views.search_by_tag)
]