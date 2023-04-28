from functools import reduce
from django import forms
from django.db.migrations.state import get_related_models_tuples
from .models import Comment, CustomUser
from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate


class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = CustomUser
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

	def clean(self):
		error_list = []
		password = self.cleaned_data.get('password1')
		password_repeat = self.cleaned_data.get('password2')

		if not any(char.isdigit() for char in password):
			error_list.append("Пароль должен содержать хотя бы 1 цифру.")
		if len(password) < 8:
			error_list.append("Длина пароля должна быть больше 8 символов.")
		if password != password_repeat:
			error_list.append("Пароли не совпадают.")

		if error_list:
			raise forms.ValidationError(error_list)	
		return self.cleaned_data
	

class MyAuthForm(AuthenticationForm):

	class Meta:
		model = CustomUser
		fields = ("username", "password")

	def clean(self):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")	
		print(1, username, password)
		if username is not None and password:
			print(2)
			self.user_cache = authenticate(
			    self.request, username=username, password=password
			)
			if self.user_cache is None:
				print(3)
				raise forms.ValidationError('Не правильно введено имя пользователя или пароль.')
			else:
				print(4)
				self.confirm_login_allowed(self.user_cache)	
		print(5)
		return self.cleaned_data

	def confirm_login_allowed(self, user):
		error_list = []
		if not user.is_active:
			error_list.append("Пользователь забанен.")
		if error_list:
			raise forms.ValidationError(error_list)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        

        fields = ['content','parent']
        
        labels = {
            'content': _(''),
        }
        
        widgets = {
            'content' : forms.TextInput(),
        }