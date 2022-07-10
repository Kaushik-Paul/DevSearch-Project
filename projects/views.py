from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages

from projects import models, forms
from projects.utils import search_project


def projects_list(request):
    context = {}

    projects, search_query = search_project(request)

    page = request.GET.get('page')

    paginator = Paginator(projects, 6)

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)

    context['title'] = 'Project List'
    context['projects'] = projects
    context['search_query'] = search_query
    context['paginator'] = paginator

    return render(request, 'projects.html', context)


def project_detail(request, pk):
    project_obj = models.Project.objects.get(pk=pk)
    # print(project_obj)
    tags = project_obj.tags.all()

    form = forms.ReviewForm()

    if request.method == 'POST':
        form = forms.ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project_obj
        review.owner = request.user.profile
        review.save()

        # Update Project Vote Count
        project_obj.get_vote_count

        messages.success(request, 'Your Review was Successfully Submitted!!')
        return redirect('project-detail', pk=pk)

    context = {'project': project_obj, 'tags': tags, 'title': 'Project Details', 'form': form}

    return render(request, 'project_detail.html', context)


@login_required(login_url='login')
def project_create(request):
    profile = request.user.profile

    context = {}
    form = forms.ProjectForm()
    context['title'] = 'Add Project'
    context['form'] = form

    if request.method == 'POST':
        form = forms.ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()

            return redirect('project-list')

    return render(request, 'project_forms.html', context)


@login_required(login_url='login')
def project_update(request, pk):
    profile = request.user.profile

    project = profile.project_set.get(pk=pk)

    context = {}
    form = forms.ProjectForm(instance=project)
    context['title'] = 'Update Project'
    context['form'] = form

    if request.method == 'POST':
        form = forms.ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('user-account')

    return render(request, 'project_forms.html', context)


@login_required(login_url='login')
def project_delete(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(pk=pk)

    context = {'title': 'Delete Project', 'object': project.title}

    if request.method == 'POST':
        project.delete()
        return redirect('user-account')

    return render(request, 'delete_template.html', context)
