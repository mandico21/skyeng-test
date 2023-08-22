from typing import List

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, UpdateView

from files.forms import FileForm
from files.models import FileUpload


class Files(ListView):
    model = FileUpload
    template_name = 'users/profile.html'
    context_object_name = 'files'

    def get_queryset(self) -> List[FileUpload]:
        return FileUpload.objects.filter(
            user=self.request.user,
            is_deleted=False
        ).all()


def file_detail(request: HttpRequest, file_id: int) -> HttpResponse:
    file = FileUpload.objects.filter(pk=file_id).first()
    return render(
        request=request,
        template_name='file/file.html',
        context={'file': file},
    )


def file_delete(request: HttpRequest, file_id: int) -> HttpResponse:
    file = FileUpload.objects.filter(pk=file_id).first()
    file.is_deleted = True
    file.status = 'deleted'
    file.save()
    return HttpResponseRedirect(reverse_lazy('users:profile'))


class FileAdd(FormView):
    form_class = FileForm
    model = FileUpload
    template_name = 'file/file_add.html'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form: FileForm):
        form = form.save(commit=False)
        form.user = self.request.user
        form.save()
        return super().form_valid(form)


class FileUpdate(UpdateView):
    model = FileUpload
    fields = ['filename', 'file']
    template_name = 'file/file_update.html'
    success_url = reverse_lazy('users:profile')
