from django.shortcuts import render
from django.utils import timezone
from .models import (
    CV,
    Experience,
    Education,
    CommunityInvolvement,
    About,
)


def about(request):
    about = About.objects.latest("published_date")
    return render(request, 'portfolio/about', {'content': about})

def cv(request):
    cv = CV.objects.latest("published_date")
    experiences = cv.experience_set.all()
    educations = cv.education_set.all()
    community_work = cv.communityinvolvement_set.all()

    context = {
        "cv": cv,
        "experiences": experiences,
        "educations": educations,
        "community_work": community_work,
    }
    return render(request, "portfolio/cv.html", context)