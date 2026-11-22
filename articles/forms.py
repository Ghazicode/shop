from django import forms
from .models import Comment



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['fullname', 'comment']
        widgets={
            'fullname':forms.TextInput(
                attrs={
                        'class':'form-control',
                    'id':'c-name',
                    'placeholder':'نام و نام خانوادگی خود را وارد نمایید'
                }
            ),
            'comment':forms.Textarea(
                attrs={
                    'class':'form-control',
                    'id':'c-text',
                    'placeholder':'ننظر خود را با ما به اشتراک بگذارید',
                    'rows':4
                }
            )
        }

        