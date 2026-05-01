from django.urls import path
from .views import AnnonceListView, AnnonceCreateView, AnnonceDetailView, AnnonceUpdateView, AnnonceDeleteView, AddCommentView

urlpatterns = [
    path('', AnnonceListView.as_view(), name='annonce_list'),
    path('create/', AnnonceCreateView.as_view(), name='annonce_create'),
    path('<int:pk>/', AnnonceDetailView.as_view(), name='annonce_detail'),
    path('<int:pk>/edit/', AnnonceUpdateView.as_view(), name='annonce_edit'),
    path('<int:pk>/delete/', AnnonceDeleteView.as_view(), name='annonce_delete'),
    path('<int:pk>/comment/', AddCommentView.as_view(), name='add_comment'),
]