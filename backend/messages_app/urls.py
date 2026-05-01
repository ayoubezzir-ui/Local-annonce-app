from django.urls import path
from .views import InboxView, ComposeMessageView, MessageDetailView

urlpatterns = [
    path('', InboxView.as_view(), name='inbox'),
    path('compose/', ComposeMessageView.as_view(), name='compose_message'),
    path('<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
]
