from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('signup-page/', views.signuppage, name='signuppage'),
    path('signin/', views.signin, name='signin'),
    path('signin-page/', views.signinpage, name='signinpage'),
    path('logout/', views.logout_view, name='logout'),

    path('user/', views.user, name='user'),
    path('user/bot_search', views.bot_search, name='bot_search'),  # ✅ updated path
    path('generate-image/', views.generate_image, name='generate_image'),

    path('pdf/', views.pdf_view, name='pdf'),
]
