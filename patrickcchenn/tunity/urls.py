from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("all", views.all, name="all"),
    path("applied", views.applied_page, name="applied_page"),
    path("register", views.register, name="register"),
    path("register/personal", views.registerP, name="personal"),
    path("register/startup", views.registerS, name="startup"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("find", views.find, name="find"),
    path("edit_profile", views.edit_profile, name="edit_profile"),
    path("profile/<str:name>", views.profile, name="profile"),
    path("post_job", views.post_job, name="post_job"),
    path("view/<str:company_name>/<int:job_id>", views.job_view, name="job_view"),
    path("acceptance", views.acceptance, name="acceptance"),


    # API
    path("apply/<int:job_id>", views.apply, name="apply"),
    # accept/decline applications
    path("update/<str:userr>/<int:vacancy_id>", views.update, name="update"),
    # jquery for search
    path("find_api/<str:query>", views.find_api, name="find"),
    # get company name
    path("get/<int:query>", views.get_api, name="get"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
