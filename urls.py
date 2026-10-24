
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("upload/", views.upload_document, name="upload_document"),
    path(
        "download/<int:document_id>/",
        views.download_document,
        name="download_document"
    ),
    path(
        "delete/<int:document_id>/",
        views.delete_document,
        name="delete_document"
    ),
    path("logout/", views.logout_view, name="logout"),
]
