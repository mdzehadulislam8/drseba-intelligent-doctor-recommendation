from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('style.css', views.style_css, name='style-css'),
    path('script.js', views.script_js, name='script-js'),
    path('api', views.api_root, name='api-root'),
    path('api/health', views.api_health, name='api-health'),
    path('api/options', views.api_options, name='api-options'),
    path('api/thanas/<str:district>', views.api_thanas, name='api-thanas'),
    path('api/recommendations', views.api_recommendations, name='api-recommendations'),
]
