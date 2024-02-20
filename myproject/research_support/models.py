from django.db import models

# Create your models here.
        


class PDF(models.Model):
    file_name = models.CharField(max_length=100)
    file = models.FileField(upload_to='pdfs/')
    upload_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    text_content = models.TextField(blank=True, null=True)
    related_docs = models.ManyToManyField('self', blank=True)
    summary = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField('Tag', blank=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)  # Adjusted field
    source = models.URLField(blank=True, null=True)
    # Placeholder for fields requiring additional models or special handling
    images = models.ManyToManyField('Image', blank=True)
    vector_representation = models.TextField(blank=True, null=True)
    
    question_answer_pairs = models.TextField(blank=True, null=True)
    user_queries = models.TextField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.file_name
       
    
# class Document(models.Model):
#     document_id = models.CharField(max_length=100)
#     file_name = models.CharField(max_length=100)
#     file_path = models.CharField(max_length=100)
#     text_content = models.TextField()
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#     def __str__(self):
#         return self.file_name
    


class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    # Add other fields as necessary
  
    
  
class Image(models.Model):
    image_id = models.CharField(max_length=100)
    document_id = models.CharField(max_length=100)
    file_path = models.CharField(max_length=100)
    associated_text = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.image_id
    
class Summary(models.Model):
    summary_id = models.CharField(max_length=100)
    document_id = models.CharField(max_length=100)
    summary = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.summary_id
    
class Tag(models.Model):
    tag_id = models.CharField(max_length=100)
    document_id = models.CharField(max_length=100)
    tag = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.tag_id

class Related(models.Model):
    related_id = models.CharField(max_length=100)
    document_id = models.CharField(max_length=100)
    related_document_id = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.related_id

class Vector(models.Model):
    vector_id = models.CharField(max_length=100)
    document_id = models.CharField(max_length=100)
    vector = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.vector_id
    
class QA(models.Model):
    qa_id = models.CharField(max_length=100)
    document_id = models.CharField(max_length=100)
    question = models.TextField()
    answer = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.qa_id

class Feedback(models.Model):
    feedback_id = models.CharField(max_length=100)
    document_id = models.CharField(max_length=100)
    feedback = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.feedback_id

class Query(models.Model):
    query_id = models.CharField(max_length=100)
    document_id = models.CharField(max_length=100)
    query = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.query_id
#
#

    
