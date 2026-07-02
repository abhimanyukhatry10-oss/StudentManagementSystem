from django.shortcuts import render, redirect, get_object_or_404
from .forms import StudentForm
from .models import Student
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse


print("VIEWS.PY LOADED")
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

def student_list(request):
    print("STUDENT LIST FUNCTION CALLED")
    return HttpResponse("Student List View Working")
#def student_list(request):

    # Database se saare students lao
    #students = Student.objects.all().order_by('id')
    #print('hello')
    #print(students,"hello")
    # Har page par 5 students
    #paginator = Paginator(students, 5)

    # URL se page number lo
    #page_number = request.GET.get('page')

    # Current page ka data
    #page_obj = paginator.get_page(page_number)
    #print("Total Students =", students.count())
    #print(page_obj)
    #print(list(page_obj))
    #context = {
     #   'students': students
    #}

    #return render(
      #  request,
       # 'students/student_list.html',
     #   context
    #)

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

def student_list(request):

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