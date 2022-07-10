from django.db.models import Q

from projects import models


def search_project(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    print("SEARCH: ", search_query)

    tags = models.Tag.objects.filter(name__icontains=search_query)

    projects = models.Project.objects.distinct().filter(Q(title__icontains=search_query) |
                                                        Q(tags__in=tags) |
                                                        Q(owner__name__icontains=search_query))

    return projects, search_query
