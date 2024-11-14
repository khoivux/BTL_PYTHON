from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'gender', 'address', 'dob']
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # Chặn không cho cập nhật email
        self.fields['email'] = forms.EmailField(
            initial=kwargs['instance'].user.email,  # Thiết lập giá trị ban đầu
            disabled=True  # Chặn chỉnh sửa
        )