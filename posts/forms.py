from django import forms
from .models import Post, Comment, Review

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'post_type', 'visibility']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating']


# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ['text', 'is_public']
#         labels = {
#             'text': 'Post Content',
#             'is_public': 'Public Post',
#         }
#         widgets = {
#             'text': forms.Textarea(attrs={'rows': 4}),
#         }
