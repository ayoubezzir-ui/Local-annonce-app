from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Message
from .forms import MessageForm

class InboxView(LoginRequiredMixin, View):
    def get(self, request):
        messages_recus = Message.objects.filter(destinataire=request.user).order_by('-date_envoi')
        messages_envoyes = Message.objects.filter(expediteur=request.user).order_by('-date_envoi')
        return render(request, 'messages_app/inbox.html', {
            'messages_recus': messages_recus,
            'messages_envoyes': messages_envoyes
        })

class ComposeMessageView(LoginRequiredMixin, View):
    def get(self, request):
        to_user_id = request.GET.get('to')
        initial_data = {}
        if to_user_id:
            initial_data['destinataire'] = to_user_id
        form = MessageForm(initial=initial_data)
        return render(request, 'messages_app/compose.html', {'form': form})

    def post(self, request):
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.expediteur = request.user
            message.save()
            return redirect('inbox')
        return render(request, 'messages_app/compose.html', {'form': form})

class MessageDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        message = get_object_or_404(Message, pk=pk)
        if message.destinataire == request.user and not message.est_lu:
            message.est_lu = True
            message.save()
        return render(request, 'messages_app/message_detail.html', {'message': message})
