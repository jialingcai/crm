from django import forms
from crm import models
from django.core.exceptions import ValidationError
import hashlib


class BootStrapForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class RegForm(BootStrapForm):
    password = forms.CharField(min_length=6, label="密码", widget=forms.PasswordInput)
    re_password = forms.CharField(min_length=6, label="确认密码", widget=forms.PasswordInput)

    class Meta:
        model = models.UserProfile     # 数据库
        fields = '__all__'   # 要显示的字段
        exclude = ["is_active"]  # 不显示的字段
        labels = {
            # 需要显示的中文名
            # "password": "密码"
        }
        widgets = { # HTML插件
            # 'password': forms.PasswordInput(attrs={'class': 'form-control'})
        }
        error_messages = {
            'username': {
                "required": "不能为空",
                "invalid": "格式错误"
            }
        }

    def clean(self):
        pwd = self.cleaned_data.get("password")
        re_pwd = self.cleaned_data.get("re_password")

        if pwd != re_pwd:
            self.add_error('re_password', "两次密码不一致")
            raise ValidationError("两次密码不一致")
        md5 = hashlib.md5()
        md5.update(pwd.encode("utf8"))
        pwd = md5.hexdigest()
        self.cleaned_data["password"] = pwd
        return self.cleaned_data


class UserForm(BootStrapForm):

    class Meta:
        model = models.Customer
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].widget.attrs = {}


class ConsultForm(BootStrapForm):

    class Meta:
        model = models.ConsultRecord
        fields = "__all__"

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields["customer"].choices = [(i.pk, str(i)) for i in self.instance.consultant.customers.all()]
        self.fields["consultant"].choices = [(self.instance.consultant.pk,self.instance.consultant.name)]


class EnrollmentForm(BootStrapForm):

    class Meta:
        model = models.Enrollment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.customer_id != '0':
            self.fields["customer"].choices=[(self.instance.customer_id,str(self.instance.customer))]
            self.fields["enrolment_class"].choices = [(i.pk, str(i)) for i in self.instance.customer.class_list.all()]