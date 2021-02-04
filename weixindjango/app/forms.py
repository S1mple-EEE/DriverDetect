from app.models import User

from django.forms import ModelForm

class MountForm(ModelForm):
  class Meta:
      model = User
      fields = '__all__'