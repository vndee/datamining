from django.urls import path
from datamining import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('associationrule', views.association_rule, name='associationrule'),
    path('decisiontree', views.decision_tree, name='decisiontree'),
]
