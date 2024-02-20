from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('research-support/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('search/', views.search, name='search'),
    path('upload/', views.upload, name='upload'),
    path('document/<int:document_id>/', views.document, name='document'),
    path('document/<int:document_id>/delete/', views.delete_document, name='delete_document'),
    path('document/<int:document_id>/summary/', views.summary, name='summary'),
    path('document/<int:document_id>/tag/', views.tag, name='tag'),
    path('document/<int:document_id>/related/', views.related, name='related'),
    path('document/<int:document_id>/vector/', views.vector, name='vector'),
    path('document/<int:document_id>/qa/', views.qa, name='qa'),
    path('document/<int:document_id>/feedback/', views.feedback, name='feedback'),
    path('document/<int:document_id>/query/', views.query, name='query'),
    path('document/<int:document_id>/pdf/', views.pdf_detail, name='pdf_detail'),
    path('document/<int:document_id>/pdf/download/', views.download_pdf, name='download_pdf'),
    path('document/<int:document_id>/pdf/delete/', views.delete_pdf, name='delete_pdf'),
    path('document/<int:document_id>/image/', views.image, name='image'),
    path('document/<int:document_id>/image/delete/', views.delete_image, name='delete_image'),
    path('document/<int:document_id>/image/download/', views.download_image, name='download_image'),
]
