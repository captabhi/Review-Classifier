from django.urls import include,path
from . import views
from django.contrib.auth import views as auth_view
app_name = 'review_classifier'

urlpatterns = [
    path('', views.showItems, name='showitems'),
    path('(?P<pk>\d+)/',views.viewitem,name='viewitem'),
    path('trainmodel/',views.makeCorpus,name='train _model'),
    #path('initial_training/', views.insertData, name='insert_data'),
    path('login/',auth_view.LoginView.as_view(template_name='review_classifier/login.html'),name='login'),
    path('logout/',auth_view.LogoutView.as_view(template_name='review_classifier/logout.html'),name='logout'),
    path('dashboard/',views.predictNewReviews,name='dashboard')

]