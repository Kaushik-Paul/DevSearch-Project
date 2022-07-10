from django.db.models import Q

from users import models


def search_profile(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    print("SEARCH: ", search_query)

    skills = models.Skill.objects.filter(name__icontains=search_query)

    profiles = models.Profile.objects.distinct().filter(Q(name__icontains=search_query) |
                                                        Q(short_intro__icontains=search_query) |
                                                        Q(skill__in=skills))

    return profiles, search_query
