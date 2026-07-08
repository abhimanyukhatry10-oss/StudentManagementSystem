from django.shortcuts import render, redirect, get_object_or_404
from .forms import StudentForm
from .models import Student
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
#from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


class StudentCreateView(LoginRequiredMixin,CreateView): #CBV me decorator nahi lagta.
    #Uski jagah Mixin use hota hai.
    #Mixin pehle kyun likha?Ye bahut important hai.
    #kyunki Python multiple inheritance me left to right search karta hai.
    model = Student
    form_class = StudentForm
    template_name = "students/add_student.html"
    success_url = reverse_lazy("student_list")

    extra_context = {
        "page_title": "Add Student",
        "button_text": "Save"
    }

    def form_valid(self, form): #Jab user valid data submit karega, tab ye method call hoga.

        print("Form is valid!")
        #form.instance.created_by = self.request.user
        #Ye wahi object hai jo save hone wala hai.Hum save se pehle usme values set kar sakte hain.
        return super().form_valid(form) #internally ye karta hai:form.save() redirect, dono ka kaam karta hai.

@login_required
def add_student(request):

    if request.method == 'POST':
        form = StudentForm(request.POST)

        if form.is_valid():
            student = form.save() #jo object abhi database me save hua hai, form.save() use return krta hai.

            messages.success(
                request,
                f'Student "{student.name}" added successfully.'
                )

            return redirect('student_list')

    else:
        form = StudentForm() #GET request

    return render(
    request,
    'students/add_student.html',
    {
        'form': form,
        'title': 'Add Student',
        'button_text': 'Save Student'
    }
    )


class StudentListView(LoginRequiredMixin,ListView):

    model = Student #Ye line: dekhkar Django samajh jata hai:Student.objects.all()
    context_object_name = "students"
    paginate_by = 5

    def get_queryset(self):
        print(self.request.GET)
        #return Student.objects.filter(age__gte=18)
        search = self.request.GET.get("search", "")

        students = Student.objects.all()

        if search:
            """students = students.filter(
                name__icontains=search
            )"""
            students = Student.objects.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(course__name__icontains=search))    

        return students
    
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["title"] = "Student List"

        context["total_students"] = Student.objects.count()
        context["search_query"] = self.request.GET.get("search", "")
        return context

@login_required
def student_list(request):
    print(request.user.username,'this is user')

    if request.user.is_authenticated:
        print("User Login Hai")

    else:
        print("User Login Nahi Hai")

    search_query = request.GET.get('search', '')

    students = Student.objects.all().order_by('id')

    if search_query:

        students = students.filter(
            Q(name__icontains=search_query) |
            Q(course__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    paginator = Paginator(students, 5)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query
    }

    return render(
        request,
        'students/student_list.html',
        context
    )

class StudentUpdateView(LoginRequiredMixin,UpdateView):

    model = Student

    form_class = StudentForm

    template_name = "students/add_student.html"

    success_url = reverse_lazy("student_list")
    #pk_url_kwarg = "id"
    extra_context = {
        "page_title": "Update Student",
        "button_text": "Update"
    }


@login_required
def update_student(request, id):

    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':

        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            form.save()

            messages.success(
             request,
                "Student updated successfully."
            )

            return redirect('student_list')

    else:

        form = StudentForm(instance=student)

    return render(
    request,
    'students/add_student.html',
    {
        'form': form,
        'title': 'Update Student',
        'button_text': 'Update Student'
    }
)

class StudentDeleteView(LoginRequiredMixin,DeleteView):

    model = Student

    template_name = "students/delete_student.html"

    success_url = reverse_lazy("student_list")


@login_required
def delete_student(request, id):

    student = get_object_or_404(Student, id=id)

    if request.method == "POST":

        student.delete()

        messages.success(
            request,
            "Student deleted successfully."
            )


        return redirect('student_list')

    return render(
        request,
        'students/delete_student.html',
        {
            'student': student
        }
    )

def search(request):

    search_query = request.GET.get('search', '')

    students = Student.objects.all()

    if search_query:
        #Yahan se actual search start hoti hai.
        students = students.filter(

            Q(name__icontains=search_query) | #contains for case-sensitive and icontains for case insensitive. | means OR

            Q(course__icontains=search_query)

        )

    context = {

        'students': students,

        'search_query': search_query

    }

    return render(
        request,
        'students/student_list.html',
        context
    )

class StudentDetailView(LoginRequiredMixin,DetailView):

    model = Student

    template_name = "students/student_detail.html"

    context_object_name = "student"