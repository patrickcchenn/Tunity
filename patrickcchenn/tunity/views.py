from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.http import JsonResponse
from .forms import UploadFileForm

from .models import User, company, condition, vacancy, applied,CV

import json

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        if hasattr(request.user, "is_company"):
            return HttpResponseRedirect(reverse("acceptance"))
        else:
            return HttpResponseRedirect(reverse("find"))
    else:
        return render(request, "tunity/index.html")


def all(request):
    all = vacancy.objects.all().order_by("timestamp").reverse()
    paginator = Paginator(all, 10)  # Show 10 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "tunity/all.html", {"all": page_obj})

def find(request):
    # map username to userid
    users=User.objects.all()
    list=[]
    for user in users:
        list.append({'id':user.id,'username':user.username})
        
    return render(request, "tunity/find.html",{'list':list})


def find_api(request,query):
    jobs = list(vacancy.objects.filter(position__icontains=query).values())
    return JsonResponse(jobs,safe=False)


@login_required
def post_job(request):

    if hasattr(request.user, "is_company") == True:
        if request.method == "POST":
            position = request.POST["position"]
            desc = request.POST["desc"]
            time1 = request.POST["appt1"]
            time2 = request.POST["appt2"]
            day1 = request.POST["day1"]
            day2 = request.POST["day2"]
            salary = request.POST["salary"]

            job = vacancy.objects.create(
                position=position,
                description=desc,
                starting_hour=time1,
                ending_hour=time2,
                starting_day=day1,
                ending_day=day2,
                salary=salary,
                user=request.user,
            )
            job.save()
            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "tunity/postJob.html")
    else:
        return HttpResponseRedirect(reverse("index"))


@csrf_exempt
def job_view(request, company_name, job_id):
    company_ = User.objects.get(username=company_name)
    job = vacancy.objects.get(pk=job_id)
    # CHECK IF USER ALREADY APLLIED FOR THE JOB BY CHECKING THE APPLIED MODEL OBJECT
    applied = [
        object_["user_id"]
        for object_ in job.applicants.all().values()
        if object_["user_id"] is request.user.id
    ]
    return render(
        request,
        "tunity/jobPage.html",
        {"company": company_.is_company, "job": job, "applied": applied},
    )


@login_required
def applied_page(request):
    user = User.objects.get(username=request.user)
    listt = []
    # if there is "applied" model for this user, if no, then not applied to anything yet.
    if user.applied.all():
        # Dont know why you need .all() even when you got the 'applied' object.cant access the list without .all().SMH
        applied_ = user.applied.all()[0].list.all()
        for job in applied_:
            # job applicant status
            conditionn = condition.objects.filter(user=user, job=job).exists()
            if conditionn:
                conditionnn = condition.objects.get(user=user, job=job)
                listt.append([job, conditionnn.accepted])
            else:
                listt.append([job])

    return render(request, "tunity/appliedPage.html", {"list": listt})


@login_required
def acceptance(request):
    user = User.objects.get(username=request.user)
    jobs = user.vacancies
    listt = []
    for job in jobs.all():
        for applicant in job.applicants.all():
            # catch here
            conditionn = condition.objects.filter(user=applicant.user, job=job).exists()
            if conditionn:
                conditionnn = condition.objects.get(user=applicant.user, job=job)
                listt.append([applicant.user, job, conditionnn.accepted])
            else:
                listt.append([applicant.user, job])

    return render(request, "tunity/acceptance.html", {"list": listt})


@csrf_exempt
def get_api(request,query):
    try:
        user = User.objects.get(pk=query)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    if request.method == "POST":
        return JsonResponse({"name": user.username}, status=201)

@csrf_exempt
@login_required
def apply(request, job_id):
    # CONTINUE HERE FUTURE PATRICK
    # OKAY PAST PATRICK
    try:
        job = vacancy.objects.get(pk=job_id)
    except vacancy.DoesNotExist:
        return JsonResponse({"error": "Vacancy not found."}, status=404)

    if request.method == "POST":
        data = json.loads(request.body)
        if data.get("body") is not None:
            # apply
            if not applied.objects.filter(user=request.user).exists():
                apply = applied.objects.create(user=request.user)
                apply.list.add(job)
            else:
                apply = applied.objects.get(user=request.user)
                apply.list.add(job)
            apply.save()

        return HttpResponse(status=204)


@csrf_exempt
@login_required
def update(request, userr, vacancy_id):

    try:
        job = vacancy.objects.get(pk=vacancy_id)
    except vacancy.DoesNotExist:
        return JsonResponse({"error": "Vacancy not found."}, status=404)
    try:
        user = User.objects.get(username=userr)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    if request.method == "POST":
        data = json.loads(request.body)
        if data.get("user") is not None and data.get("vacancy_id") is not None:
            # apply
            if data.get("condition"):
                # create condition model object
                create = condition.objects.create(accepted=True, job=job, user=user)
            else:
                create = condition.objects.create(accepted=False, job=job, user=user)
            create.save()

        return HttpResponse(status=204)


@login_required
def profile(request, name):
    user = User.objects.get(username=name)
    # ensure privacy, users cant access others personal profile
    list = []
    # # get list of applied vacancy and condition for personal account
    if not hasattr(user, "is_company"):
        return HttpResponse(status=404)
    #     applied_object=applied.objects.get(user=request.user)
    #     for item in applied_object.list.all():
    #         list.append(item)

    return render(request, "tunity/profile.html", {"owner": user})


def register(request):
    return render(request, "tunity/register.html")


def registerP(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request,
                "tunity/registerPersonal.html",
                {"message": "Passwords must match."},
            )

        
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            
        except IntegrityError:
            return render(
                request,
                "tunity/registerPersonal.html",
                {"message": "Username already taken."},
            )

        # Create new CV
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = CV(user=user,file_field=request.FILES['file'])
            instance.save()
            user.save()

        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        form= UploadFileForm()
        return render(request, "tunity/registerPersonal.html",{'form': form})


def registerS(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        year = request.POST["year"]
        body = request.POST["about"]
        country = request.POST["country"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request,
                "tunity/registerStartup.html",
                {"message": "Passwords must match."},
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            comp = company.objects.create(
                year=year, body=body, country=country, user=user
            )
            comp.save()
        except IntegrityError:
            return render(
                request,
                "tunity/registerStartup.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "tunity/registerStartup.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "tunity/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "tunity/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@login_required
def edit_profile(request):
    if request.method == "POST":
        email = request.POST["email"]
        year = request.POST["year"]
        body = request.POST["about"]
        country = request.POST["country"]
        comp = company.objects.get(user=request.user)

        comp.email = email
        comp.year = year
        comp.body = body
        comp.country = country
        comp.save()

        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "tunity/registerStartup.html", {"user": request.user})
