from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from SolarTumbler.models import LogEntry, Group, Comment, Fav
from SolarTumbler.forms import GroupForm, CommentForm

# Create your views here.


class LogEntryList(LoginRequiredMixin, View):
    def get(self, request):
        mc = Group.objects.all().count()
        al = LogEntry.objects.all()
        favorites = list()
        if request.user.is_authenticated:
            rows = request.user.favorite_logentrys.values('id')
            favorites = [ row['id'] for row in rows ]
        ctx = {'group_count': mc, 'logentry_list': al, 'favorites': favorites}
        return render(request, 'SolarTumbler/logentry_list.html', ctx)

class LogEntryDetailView(LoginRequiredMixin, View):
    model = LogEntry
    template_name = "SolarTumbler/logentry_detail.html"
    def get(self, request, pk) :
        x = LogEntry.objects.get(id=pk)
        comments = Comment.objects.filter(logentry=x).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'logentry' : x, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        f = get_object_or_404(LogEntry, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, logentry=f)
        comment.save()
        return redirect(reverse('SolarTumbler:logentry_detail', args=[pk]))

class GroupView(LoginRequiredMixin, View):
    def get(self, request):
        ml = Group.objects.all()
        ctx = {'group_list': ml}
        return render(request, 'SolarTumbler/group_list.html', ctx)


# We use reverse_lazy() because we are in "constructor attribute" code
# that is run before urls.py is completely loaded
class GroupCreate(LoginRequiredMixin, View):
    template = 'SolarTumbler/group_form.html'
    success_url = reverse_lazy('SolarTumbler:all')

    def get(self, request):
        form = GroupForm()
        ctx = {'form': form}
        return render(request, self.template, ctx)

    def post(self, request):
        form = GroupForm(request.POST)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template, ctx)

        group = form.save()
        return redirect(self.success_url)


# GroupUpdate has code to implement the get/post/validate/store flow
# LogEntryUpdate (below) is doing the same thing with no code
# and no form by extending UpdateView
class GroupUpdate(LoginRequiredMixin, View):
    model = Group
    success_url = reverse_lazy('SolarTumbler:all')
    template = 'SolarTumbler/group_form.html'

    def get(self, request, pk):
        group = get_object_or_404(self.model, pk=pk)
        form = GroupForm(instance=group)
        ctx = {'form': form}
        return render(request, self.template, ctx)

    def post(self, request, pk):
        group = get_object_or_404(self.model, pk=pk)
        form = GroupForm(request.POST, instance=group)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template, ctx)

        form.save()
        return redirect(self.success_url)


class GroupDelete(LoginRequiredMixin, View):
    model = Group
    success_url = reverse_lazy('SolarTumbler:all')
    template = 'SolarTumbler/group_confirm_delete.html'

    def get(self, request, pk):
        group = get_object_or_404(self.model, pk=pk)
        form = GroupForm(instance=group)
        ctx = {'group': group}
        return render(request, self.template, ctx)

    def post(self, request, pk):
        group = get_object_or_404(self.model, pk=pk)
        group.delete()
        return redirect(self.success_url)


# Take the easy way out on the main table
# These views do not need a form because CreateView, etc.
# Build a form object dynamically based on the fields
# value in the constructor attributes
# class LogEntryCreate(LoginRequiredMixin, CreateView):
#     model = LogEntry
#     fields = ['item','group']
#     success_url = reverse_lazy('SolarTumbler:all')

class LogEntryCreate(LoginRequiredMixin, CreateView):
        model = LogEntry
        fields = ['item','group','owner']
        success_url = reverse_lazy('SolarTumbler:all')

class LogEntryUpdate(LoginRequiredMixin, UpdateView):
    model = LogEntry
    fields = ['item','group','owner']
    success_url = reverse_lazy('SolarTumbler:all')


class LogEntryDelete(LoginRequiredMixin, DeleteView):
    model = LogEntry
    fields = '__all__'
    success_url = reverse_lazy('SolarTumbler:all')

# We use reverse_lazy rather than reverse in the class attributes
# because views.py is loaded by urls.py and in urls.py as_view() causes
# the constructor for the view class to run before urls.py has been
# completely loaded and urlpatterns has been processed.

# References

# https://docs.djangoproject.com/en/3.0/ref/class-based-views/generic-editing/#createview

# csrf exemption in class based views
# https://stackoverflow.com/questions/16458166/how-to-disable-djangos-csrf-validation
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Add PK",pk)
        t = get_object_or_404(LogEntry, id=pk)
        fav = Fav(owner=request.user, logentry=t)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Delete PK",pk)
        t = get_object_or_404(LogEntry, id=pk)
        try:
            fav = Fav.objects.get(owner=request.user, logentry=t).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()