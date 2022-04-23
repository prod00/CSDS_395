from urllib import request
from django.contrib import messages

from django.shortcuts import get_object_or_404, redirect, render

from django.views.generic import TemplateView
from .decorators import student_required, professor_required

from .forms import  TAApplicationForm, RAApplicationForm
from .models import User, Student, Professor, TAPositionPost, TAApplication, Courses, Departments, StudentInterests, TAPositionChat, RAPositionChat, RAPositionPost, RAApplication

from django.conf import settings
from django.core.mail import send_mail

# Global variable needed to get show all posts feature to work
showall = False


def home(request):
    if request.user.is_authenticated:
        if request.user.is_student:
            return redirect('student_home')
        elif request.user.is_professor:
            return redirect('professor_home')
        else:
            return render(request, 'registration/signup.html')
    else:
        return render(request, 'applicase/landing_page.html')


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'



@student_required
def student_home(request):
    ta_posts = TAPositionPost.objects.all().order_by('-date_posted')
    all_ra_posts = RAPositionPost.objects.all().order_by('-date_posted')

    student_applications = TAApplication.objects.filter(user=request.user.student).order_by('-date_applied')
    student_applications_ra = RAApplication.objects.filter(user=request.user.student).order_by('-date_applied')

    ta_application_form = TAApplicationForm()
    ra_application_form = RAApplicationForm()

    user_interests = []

    posts = []
    applications = []

    ra_posts = []
    ra_applications = []

    interests = StudentInterests.objects.filter(username = request.user.username).values("interest")
    for interest in interests:
        interest = list(interest.values())[0]
        user_interests.append(interest)

    for post in all_ra_posts:
        ra_posts.append(post)

    if showall:
        for post in ta_posts:
            posts.append(post)
    else:
        for post in ta_posts:
            for ui in user_interests:
                if ui in post.department:
                    posts.append(post)

    for app in student_applications:
        for post in posts:
            if post.id == app.position.id:
                applications.append(app)
                posts.remove(post)

    for app in student_applications_ra:
        for ra_post in ra_posts:
            if ra_post.id == app.position.id:
                ra_applications.append(app)
                ra_posts.remove(ra_post)


    ta_app = False
    ra_app = False
    post_id = None

    if request.method == 'POST':
        for key, value in request.POST.items():
            print(key,value)
            if 'post_id' in key:
                post_id = key.replace('post_id', '')
            if 'message' in key:
                print("ra")
                ra_app = True
            if 'taken' in key:
                print("ta")
                ta_app = True

        if ta_app:
            new_ta_application_form = TAApplicationForm(request.POST)
            if new_ta_application_form.is_valid():
                user = request.user.student
                position = TAPositionPost.objects.get(id=int(post_id))
                taken = new_ta_application_form.cleaned_data['taken']
                grade = new_ta_application_form.cleaned_data['grade']
                float_year = new_ta_application_form.cleaned_data['year']
                if int(float_year) != float_year:
                    semester = "fall"
                else:
                    semester = "spring"
                year = int(float_year)
                professor = new_ta_application_form.cleaned_data['professor']
                comment = new_ta_application_form.cleaned_data['comment']

                new_application = TAApplication.objects.create(user=user,
                                                               position=position,
                                                               taken=taken,
                                                               grade=grade,
                                                               year=year,
                                                               semester=semester,
                                                               professor=professor,
                                                               comment=comment)
                new_application.save()
                messages.success(request, 'The TA application for ' + str(position.section) + ' has been sent!')
                subject = 'New Applicase Response'
                message = f'Hi Professor {position.user.last_name}, a new student has applied to your ' \
                          f'{position.section} Teaching Assistant post.'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [position.user.email,]
                send_mail(subject, message, email_from, recipient_list)
                return redirect('student_home')

        elif ra_app:
            new_ra_application_form = RAApplicationForm(request.POST)
            if new_ra_application_form.is_valid():
                print("making new")
                user = request.user.student
                position = RAPositionPost.objects.get(id=int(post_id))
                message = new_ra_application_form.cleaned_data['message']
                new_application = RAApplication.objects.create(user=user, position=position, comment=message)
                new_application.save()

                messages.success(request, 'The RA application for ' + str(position.title) + ' has been sent!')
                print("created")
                return redirect('student_home')

    context = {
        'ta_posts': posts,
        'ra_posts': ra_posts,
        'ta_application_form': ta_application_form,
        'ra_application_form': ra_application_form,
        'ta_applications': applications,
        'ra_applications': ra_applications,

    }
    return render(request, 'applicase/student_home.html', context)
    # return render(request, 'applicase/index.html', context)


@professor_required
def professor_home(request):
    classes = Courses.objects.all()
    departments = Departments.objects.all()
    print(departments.all())
    ta_professor_posts = TAPositionPost.objects.filter(user=request.user).order_by('-date_posted')
    ra_professor_posts = RAPositionPost.objects.filter(user=request.user).order_by('-date_posted')
    context = {
        #'ta_post_form': ta_post_form,
        'ta_posts': ta_professor_posts,
        'ra_posts': ra_professor_posts,
        'classes': classes,
        'departments': departments,
    }
    return render(request, 'applicase/professor_home.html', context)

def studentuniqueID(request):
    messages.success(request, 'Case ID must be unique')
    return redirect('student_signup')


def is_student(request):
    user = request.user
    new_user = Student(user=user, first_name=user.first_name, last_name=user.last_name,
                                      case_id=user.username)

    user.is_student = True
    user.is_professor = False
    user.save()
    new_user.save()
    print(user.is_student)
    return redirect('student_home')


def is_professor(request):
    user = request.user
    new_professor = Professor(user=user, first_name=user.first_name, last_name=user.last_name,
                                        case_id=user.username)
    user.is_professor = True
    user.is_student = False
    user.save()
    new_professor.save()
    return redirect('professor_home')


# class ProfessorSignUpView(CreateView):
#     model = User
#     form_class = ProfessorSignUpForm
#     template_name = 'registration/signup_form.html'
#
#     def get_context_data(self, **kwargs):
#         kwargs['user_type'] = 'professor'
#         return super().get_context_data(**kwargs)
#
#     def form_valid(self, form):
#         login(self.request, form.save())
#         return redirect('professor_home')

def StudentInterestsView(request):
    departments = Departments.objects.all().order_by('department')
    currentInterests = StudentInterests.objects.filter(username = request.user.username)
    context = {
        'departments': departments,
        'interests': currentInterests,
        'showAll': showall
    }
    return render(request, 'applicase/interests_form.html', context)



def ta_post_submit(request):
    #position_form = TAPositionPostForm(request.POST)
    if request.method == 'POST':
        section = request.POST['classes']
        description = request.POST['description']
        courseCode = section.split(":")[0].strip()
        user = request.user
        if Courses.objects.filter(code = courseCode).exists():
            department = Courses.objects.filter(code = courseCode).values("department")[0]['department'].strip()
            new_position = TAPositionPost.objects.create(section=section, description=description, user=user, department = department)
            new_position.save()
        else:
            new_position = TAPositionPost.objects.create(section=section, description=description, user=user)
            new_position.save()

        new_chat = TAPositionChat.objects.create(position=new_position)
        new_chat.members.add(request.user)
        new_chat.save()
    messages.success(request, 'The TA position has been posted!')
    return redirect('professor_home')

def ra_post_submit(request):
    if request.method == 'POST':
        title = request.POST['title']
        department = request.POST['department']
        key_words = request.POST['key_words']
        description = request.POST['description']
        user = request.user

        new_position = RAPositionPost.objects.create(user=user,
                                                     title=title,
                                                     department=department,
                                                     key_words=key_words,
                                                     description=description)
        new_position.save()

        new_chat = RAPositionChat.objects.create(position=new_position)
        new_chat.members.add(request.user)
        new_chat.save()
    messages.success(request, 'The RA position has been posted!')
    return redirect('professor_home')



@professor_required
def ta_applications(request, pk=1):

    ta_apps = TAApplication.objects.filter(position__user=request.user, position_id=pk).order_by('-date_applied')
    post = TAPositionPost.objects.get(pk=pk)
    context = {"applications": ta_apps,
               "post": post}
    return render(request, 'applicase/professor_TAapplications.html', context)


@professor_required
def ra_applications(request, pk=1):

    ra_apps = RAApplication.objects.filter(position__user=request.user, position_id=pk).order_by('-date_applied')
    post = RAPositionPost.objects.get(pk=pk)
    context = {"applications": ra_apps,
               "post": post}
    return render(request, 'applicase/professor_RAapplications.html', context)

def student_interest_update(request):
    global showall
    showall = eval(request.POST.getlist("showAll")[0])
    interests = request.POST.getlist("interests")
    oldInterests = StudentInterests.objects.filter(username = request.user.username)
    oldInterests.delete()
    for interest in interests:
        new_interest = StudentInterests.objects.create(username = request.user.username, interest = interest)
        new_interest.save()
    return redirect('student_home')

def add_user_to_ta_chat(request, pk):
    ta_application = TAApplication.objects.get(pk=pk)
    position_id = ta_application.position.id
    ta_chat = TAPositionChat.objects.get(position_id=position_id)
    ta_chat.members.add(ta_application.user.user)
    ta_chat.save()
    return redirect("room", str(position_id))

def add_user_to_ra_chat(request, pk):
    ra_application = RAApplication.objects.get(pk=pk)
    position_id = ra_application.position.id
    ra_chat = RAPositionChat.objects.get(position_id=position_id)
    ra_chat.members.add(ra_application.user.user)
    ra_chat.save()
    return redirect("room", str(position_id))

def user_chats(request):
    user_chat_streams = []
    for chat in TAPositionChat.objects.all():
        for member in chat.members.all():
            if request.user == member:
                user_chat_streams.append(chat)
    context = {"chats": user_chat_streams,}
    return render(request, "applicase/chats.html", context)