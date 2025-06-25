from django.shortcuts import get_object_or_404, redirect, render
from apps.customers.models import Client, Activity
from django.views.generic import DetailView
from apps.customers.forms import ClientForm

def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)
    form = ClientForm(request.POST or None, instance=client)
    if form.is_valid():
        form.save()
        Activity.objects.create(
            contact=client,
            user=request.user,
            event_type="updated",
            note="Changed address & phone"
        )
        return redirect("customers:detail", pk=client.pk)
    return render(request, "customers/client_form.html", {"form": form})



class ClientDetailView(DetailView):
    model = Client
    template_name = "customers/client_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # pull in that contact’s activities
        ctx["activities"] = self.object.activities.all()
        return ctx

def client_detail(request, pk):
    client     = get_object_or_404(Client, pk=pk)
    activities = Activity.objects.filter(contact=client)
    return render(
        request,
        "customers/detail.html",
        {
            "client":     client,
            "activities": activities,
        }
    )

class TimelineView(DetailView):
    model = Client
    template_name = "activity/timeline.html"
    context_object_name = "client"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # pull in all past activities for this client
        ctx["activities"] = self.object.activities.all()
        return ctx