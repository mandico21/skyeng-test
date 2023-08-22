from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from files.models import FileUpload
from users.forms import RegisterForm


@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    files = (FileUpload.objects.filter(
        user=request.user,
        is_deleted=False
    ).order_by(
        'created_at'
    ).all())
    return render(
        request,
        template_name='users/profile.html',
        context={'files': files}
    )


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
