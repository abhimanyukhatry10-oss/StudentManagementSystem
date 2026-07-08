
from django.urls import path
from . import views

urlpatterns = [

    #path('add/', views.add_student, name='add_student'),
    #path('', views.student_list, name='student_list'),
    #path('update/<int:id>/', views.update_student, name='update_student'),
    #path('delete/<int:id>/', views.delete_student, name='delete_student'),
    path('',views.StudentListView.as_view(),name='student_list'),
    path('add/',views.StudentCreateView.as_view(),name='add_student'),
    path("update/<int:pk>/",views.StudentUpdateView.as_view(),name="update_student"),
    path("delete/<int:pk>/",views.StudentDeleteView.as_view(),name="delete_student"),
    path("student/<int:pk>/",views.StudentDetailView.as_view(),name="student_detail")

]