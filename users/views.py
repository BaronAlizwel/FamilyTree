from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, UpdateView, View, FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CustomUserCreationForm, CustomUserChangeForm, UserSearchForm
from .models import CustomUser, UserActivity, Notification
from connections.models import Connection, ConnectionRequest 

from messaging.forms import MessageForm


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


class LoginView(auth_views.LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        # Retrieve data for the user dashboard
        connection_requests = ConnectionRequest.objects.filter(to_user=request.user, status=ConnectionRequest.PENDING)
        notifications = Notification.objects.filter(recipient=request.user, is_read=False)
        recently_connected_users = Connection.objects.filter(from_user=request.user).order_by('-from_user')[:5]
        
        # Render the dashboard template with the data
        return render(request, 'users/dashboard.html', {
            'connection_requests': connection_requests,
            'notifications': notifications,
            'recently_connected_users': recently_connected_users,
        })


class ProfileView(TemplateView):
    template_name = 'users/profile.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        user.notifications.filter(is_read=False).update(is_read=True)
        return render(request, self.template_name, {'user': user})


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_public = form.cleaned_data['is_public']
        self.object.save()
        return super().form_valid(form)


def user_detail(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    return render(request, 'users/user_detail.html', {'user': user})


class SearchUsersView(FormView):
    form_class = UserSearchForm
    template_name = 'users/search_users.html'

    def form_valid(self, form):
        search_fields = ['username', 'location', 'bio']
        users = CustomUser.objects.all()

        for field in search_fields:
            term = form.cleaned_data.get('search_term')  # Update this line
            if term:
                users = users.filter(**{f'{field}__icontains': term})

        return render(self.request, 'users/search_results.html', {'users': users})


@login_required
def view_other_profile(request):
    if request.method == 'POST':
        to_user_id = request.POST.get('to_user_id')
        to_user = get_object_or_404(CustomUser, id=to_user_id)
        ConnectionRequest.objects.create(from_user=request.user, to_user=to_user)
        return render(request, 'users/connection_request_sent.html')
    else:
        user_id = request.GET.get('user_id')
        user = get_object_or_404(CustomUser, id=user_id)
        form = MessageForm()
        return render(request, 'users/view_profile.html', {'user': user, 'form': form})
