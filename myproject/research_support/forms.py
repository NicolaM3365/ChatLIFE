from django import forms
from .models import Document, Image, Summary, Tag, Related, Vector, QA, Feedback, Query, PDF

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file']  # List all the fields you want from the model


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['document_id', 'file_path']  # List all the fields you want from the model

class SummaryForm(forms.ModelForm):
    class Meta:
        model = Summary
        fields = ['document_id', 'summary']  # List all the fields you want from the model


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['document_id', 'tag']  # List all the fields you want from the model


class RelatedForm(forms.ModelForm):
    class Meta:
        model = Related
        fields = ['document_id', 'related_document_id']  # List all the fields you want from the model


class VectorForm(forms.ModelForm):
    class Meta:
        model = Vector
        fields = ['document_id', 'vector']  # List all the fields you want from the model


class QAForm(forms.ModelForm):
    class Meta:
        model = QA
        fields = ['document_id', 'question', 'answer']  # List all the fields you want from the model


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['document_id', 'feedback']  # List all the fields you want from the model


class QueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ['document_id', 'query']  # List all the fields you want from the model


class PDFForm(forms.ModelForm):
    class Meta:
        model = PDF
        fields = ['file_name', 'text_content', 'related_docs', 'summary', 'tags', 'category', 'author', 'source', 'images', 'vector_representation', 'question_answer_pairs', 'user_queries', 'feedback']  # List all the fields you want from the model

class SearchForm(forms.Form):
    search = forms.CharField(max_length=100)

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class UploadForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
    






# Compare this snippet from myproject/research_support/views.py:
        
# def upload(request):
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)

#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('pdfs'))
#     else:
#         form = DocumentForm()



#     return render(request, 'research_support/upload.html', {
    
#         'form': form
#     })

# def upload_image(request):

#     if request.method == 'POST':

