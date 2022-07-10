from django.core.validators import ValidationError
from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from projects.models import Project
from users import models
from users.forms import CustomUserCreationForm, ProfileForm, SkillForm
from users.utils import search_profile


def profiles(request):

    # # To Get the all the skill set for a particular profile
    # profile = models.Profile.objects.get(name='Kaushik Paul')
    # for skill in profile.skill_set.all():
    #     print(skill.name)

    profiles, search_query = search_profile(request)

    page = request.GET.get('page')
    paginator = Paginator(profiles, 6)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    context = {'profiles': profiles, 'search_query': search_query, 'paginator': paginator}
    return render(request, 'profiles.html', context)


def profile_details(request, pk):
    try:
        profile = models.Profile.objects.get(pk=pk)
    except models.Profile.DoesNotExist:
        raise ValidationError("The Requested Profile Does not exist")

    skills = models.Skill.objects.filter(owner=profile)
    projects = Project.objects.filter(owner=profile)

    context = {'profile': profile, 'skills': skills, 'projects': projects}

    return render(request, 'profile_details.html', context)


def login_user(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "User Not Found!!")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.warning(request, "Either Username or Password is incorrect")

    return render(request, 'login_register.html', {'page': page})


def logout_user(request):
    logout(request)
    messages.info(request, "User was Successfully logged out")
    return redirect('login')


def register_user(request):
    context = {}
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "User Successfully Created!!")

            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(request, 'An Error has occurred while registering the User')

    context['page'] = page
    context['form'] = form

    return render(request, 'login_register.html', context)


@login_required(login_url='login')
def user_account(request):
    profile = request.user.profile

    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {'profile': profile, 'skills': skills, 'projects': projects}
    return render(request, 'account.html', context)


@login_required(login_url='login')
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('user-account')

    context = {'form': form}

    return render(request, 'profile_form.html', context)


@login_required(login_url='login')
def create_skill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was added successfully!')
            return redirect('user-account')

    context = {'form': form}
    return render(request, 'skill_form.html', context)


@login_required(login_url='login')
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was updated successfully!')
            return redirect('user-account')

    context = {'form': form}
    return render(request, 'skill_form.html', context)


@login_required(login_url='login')
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted successfully!')
        return redirect('user-account')

    context = {'object': skill}
    return render(request, 'delete_template.html', context)

