from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import CustomUser
from .forms import CustomUserCreationForm
from annonces.models import Annonce
from messages_app.models import Message

class UserCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.role == 'chef'

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'users/user_form.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        return render(request, 'users/user_form.html', {'form': form})

class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        annonces_recentes = Annonce.objects.all().order_by('-date_creation')[:5]
        messages_non_lus = Message.objects.filter(destinataire=request.user, est_lu=False).count()
        mes_annonces = Annonce.objects.filter(auteur=request.user).count()
        
        return render(request, 'users/dashboard.html', {
            'annonces_recentes': annonces_recentes,
            'messages_non_lus': messages_non_lus,
            'mes_annonces': mes_annonces,
        })

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'users/profile.html')

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login')
