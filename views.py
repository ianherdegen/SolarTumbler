from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from SolarTumbler.models import LogEntry, Item, Comment
from SolarTumbler.forms import ItemForm, CommentForm

# Create your views here.


class LogEntryList(LoginRequiredMixin, View):
    def get(self, request):
        mc = Item.objects.all().count()
        al = LogEntry.objects.all()

        ctx = {'item_count': mc, 'logentry_list': al}
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
        comment = Comment(text=request.POST['comment'], logentry=f)
        comment.save()
        return redirect(reverse('forums:forum_detail', args=[pk]))

class ItemView(LoginRequiredMixin, View):
    def get(self, request):
        ml = Item.objects.all()
        ctx = {'item_list': ml}
        return render(request, 'SolarTumbler/item_list.html', ctx)


# We use reverse_lazy() because we are in "constructor attribute" code
# that is run before urls.py is completely loaded
class ItemCreate(LoginRequiredMixin, View):
    template = 'SolarTumbler/item_form.html'
    success_url = reverse_lazy('SolarTumbler:all')

    def get(self, request):
        form = ItemForm()
        ctx = {'form': form}
        return render(request, self.template, ctx)

    def post(self, request):
        form = ItemForm(request.POST)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template, ctx)

        item = form.save()
        return redirect(self.success_url)


# ItemUpdate has code to implement the get/post/validate/store flow
# LogEntryUpdate (below) is doing the same thing with no code
# and no form by extending UpdateView
class ItemUpdate(LoginRequiredMixin, View):
    model = Item
    success_url = reverse_lazy('SolarTumbler:all')
    template = 'SolarTumbler/item_form.html'

    def get(self, request, pk):
        item = get_object_or_404(self.model, pk=pk)
        form = ItemForm(instance=item)
        ctx = {'form': form}
        return render(request, self.template, ctx)

    def post(self, request, pk):
        item = get_object_or_404(self.model, pk=pk)
        form = ItemForm(request.POST, instance=item)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template, ctx)

        form.save()
        return redirect(self.success_url)


class ItemDelete(LoginRequiredMixin, View):
    model = Item
    success_url = reverse_lazy('SolarTumbler:all')
    template = 'SolarTumbler/item_confirm_delete.html'

    def get(self, request, pk):
        item = get_object_or_404(self.model, pk=pk)
        form = ItemForm(instance=item)
        ctx = {'item': item}
        return render(request, self.template, ctx)

    def post(self, request, pk):
        item = get_object_or_404(self.model, pk=pk)
        item.delete()
        return redirect(self.success_url)


# Take the easy way out on the main table
# These views do not need a form because CreateView, etc.
# Build a form object dynamically based on the fields
# value in the constructor attributes
class LogEntryCreate(LoginRequiredMixin, CreateView):
    model = LogEntry
    fields = '__all__'
    success_url = reverse_lazy('SolarTumbler:all')


class LogEntryUpdate(LoginRequiredMixin, UpdateView):
    model = LogEntry
    fields = '__all__'
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