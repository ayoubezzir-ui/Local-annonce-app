from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, DeleteView
from .models import Annonce, Commentaire, LectureAnnonce
from .forms import AnnonceForm, CommentaireForm
from categories.models import Department

AUTHORIZED_ROLES = ['chef', 'manager', 'ingenieur']

class AnnonceListView(LoginRequiredMixin, View):
    def get(self, request):
        query = request.GET.get('q')
        departement_id = request.GET.get('departement')
        departements = Department.objects.all()
        
        annonces = Annonce.objects.all().order_by('-date_creation')
        
        if query:
            annonces = annonces.filter(Q(titre__icontains=query) | Q(contenu__icontains=query))
        
        if departement_id:
            annonces = annonces.filter(departement_id=departement_id)
            
        return render(request, 'annonces/annonce_list.html', {
            'annonces': annonces,
            'departements': departements,
            'selected': departement_id,
            'query': query,
            'can_create': request.user.role in AUTHORIZED_ROLES,
        })

class AnnonceDetailView(LoginRequiredMixin, DetailView):
    model = Annonce
    template_name = 'annonces/annonce_detail.html'
    context_object_name = 'annonce'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # Mark as read
        LectureAnnonce.objects.get_or_create(annonce=self.object, utilisateur=request.user)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentaireForm()
        context['commentaires'] = self.object.commentaires.all().order_by('-date_creation')
        context['lectures_count'] = self.object.lectures.count()
        return context

class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        annonce = get_object_or_404(Annonce, pk=pk)
        form = CommentaireForm(request.POST)
        if form.is_valid():
            commentaire = form.save(commit=False)
            commentaire.annonce = annonce
            commentaire.auteur = request.user
            commentaire.save()
        return redirect('annonce_detail', pk=pk)

class AnnonceCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.role in AUTHORIZED_ROLES

    def get(self, request):
        form = AnnonceForm()
        return render(request, 'annonces/annonce_form.html', {'form': form, 'action': 'Créer'})

    def post(self, request):
        form = AnnonceForm(request.POST, request.FILES)
        if form.is_valid():
            annonce = form.save(commit=False)
            annonce.auteur = request.user
            annonce.save()
            return redirect('annonce_list')
        return render(request, 'annonces/annonce_form.html', {'form': form, 'action': 'Créer'})

class AnnonceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Annonce
    form_class = AnnonceForm
    template_name = 'annonces/annonce_form.html'
    success_url = reverse_lazy('annonce_list')

    def test_func(self):
        annonce = self.get_object()
        return self.request.user == annonce.auteur or self.request.user.role in ['chef', 'manager']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Modifier'
        return context

class AnnonceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Annonce
    template_name = 'annonces/annonce_confirm_delete.html'
    success_url = reverse_lazy('annonce_list')

    def test_func(self):
        annonce = self.get_object()
        return self.request.user == annonce.auteur or self.request.user.role in ['chef', 'manager']