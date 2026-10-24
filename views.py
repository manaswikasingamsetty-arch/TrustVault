
import os

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404

from .models import Document
from .forms import DocumentUploadForm


def home(request):
    return render(request, "pages/home.html")


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Account created successfully! Please login."
            )
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(
        request,
        "pages/register.html",
        {"form": form}
    )


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(request, "pages/login.html")


@login_required
def dashboard(request):
    documents = Document.objects.filter(
        user=request.user
    ).order_by("-uploaded_at")

    return render(
        request,
        "pages/dashboard.html",
        {"documents": documents}
    )


@login_required
def upload_document(request):
    if request.method == "POST":
        form = DocumentUploadForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user

            uploaded_file = form.cleaned_data["file"]
            content_type = uploaded_file.content_type

            if content_type == "application/pdf":
                document.file_type = "PDF"

            elif content_type in [
                "image/jpeg",
                "image/png",
            ]:
                document.file_type = "IMAGE"

            else:
                form.add_error(
                    "file",
                    "Only PDF, JPG, JPEG and PNG files are allowed."
                )

                return render(
                    request,
                    "pages/upload.html",
                    {"form": form}
                )

            document.save()

            messages.success(
                request,
                "Document uploaded successfully!"
            )

            return redirect("dashboard")

    else:
        form = DocumentUploadForm()

    return render(
        request,
        "pages/upload.html",
        {"form": form}
    )


@login_required
def download_document(request, document_id):
    document = get_object_or_404(
        Document,
        id=document_id,
        user=request.user
    )

    if not document.file:
        raise Http404("File not found.")

    try:
        document.file.open("rb")

        return FileResponse(
            document.file,
            as_attachment=True,
            filename=os.path.basename(document.file.name)
        )

    except (OSError, ValueError):
        raise Http404("File not found.")


@login_required
@require_POST
def delete_document(request, document_id):
    document = get_object_or_404(
        Document,
        id=document_id,
        user=request.user
    )

    document.file.delete(save=False)
    document.delete()

    messages.success(
        request,
        "Document deleted successfully!"
    )

    return redirect("dashboard")


@require_POST
def logout_view(request):
    logout(request)
    return redirect("home")
