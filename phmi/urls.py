"""phmi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.Home.as_view(), name="home"),
    path("activities", views.ActivityList.as_view(), name="activity-list"),
    path("activities/<slug>", views.ActivityDetail.as_view(), name="activity-detail"),
    path("login", views.GenerateMagicLoginURL.as_view(), name="request-login"),
    path("login/<signed_pk>", views.Login.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("org-types", views.OrgTypeList.as_view(), name="org-type-list"),
    path("org-types/<slug>", views.OrgTypeDetail.as_view(), name="org-type-detail"),
]


if settings.SHOW_DATA_ACCESS:
    urlpatterns = urlpatterns + [
        path("data-access", views.DataAccessView.as_view(), name="data-access"),
        path(
            "data-access-wizard/",
            include(("data_access.urls", "data_access"), namespace="data-access"),
        ),
        path(
            "data-access2", views.DataTypeSelector.as_view(), name="data-type-selector"
        ),
        path(
            "data-access2/<pk>",
            views.DataTypeResults.as_view(),
            name="data-type-results",
        ),
        path(
            "data-access2/<pk>/activities/<activity_pk>",
            views.DataTypeActivityLegalJustifications.as_view(),
            name="data-type-activity",
        ),
        path(
            "data-access2/<pk>/organisations/<org_type_pk>",
            views.DataTypeOrgTypeLegalJustifications.as_view(),
            name="data-type-org-type",
        ),
    ]


if settings.SHOW_PROJECTS:
    urlpatterns = urlpatterns + [path("", include("activity_assessment.urls"))]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
