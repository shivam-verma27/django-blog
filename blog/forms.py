from django import forms
from .models import Post, Comment,Category

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content','categories']

    def clean_title(self):

        title = self.cleaned_data['title']

        if len(title) < 5:
            raise forms.ValidationError(
                "Title must be at least 5 characters."
            )
        forbidden_words = ['bad']
        for word in forbidden_words:
            if word in title.lower():
                raise forms.ValidationError(
                    f"Title cannot contain the word '{word}'."
                )

        return title
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
