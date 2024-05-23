from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.account.adapter import DefaultAccountAdapter

USER_FIELDS = ['username', 'nickname', 'first_name', 'last_name', 'email', 'profile_img']

class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    nickname = models.CharField(max_length=50)
    email = models.EmailField(max_length=300, blank=True, null=True)
    profile_img = models.ImageField(upload_to='image/', default='image/user.png')
    financial_products = models.TextField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    money = models.IntegerField(blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)
    desire_amount_saving = models.IntegerField(blank=True, null=True)
    desire_amount_deposit = models.IntegerField(blank=True, null=True)
    deposit_period = models.IntegerField(blank=True, null=True)
    saving_period = models.IntegerField(blank=True, null=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        from allauth.account.utils import user_email, user_field,user_username
        data = form.cleaned_data

        user_email(user, data.get('email'))
        user_username(user, data.get('username'))

        for field in USER_FIELDS:
            if data.get(field):
                setattr(user, field, data.get(field))
        
        financial_product = data.get("financial_products")
        if financial_product:
            financial_products = user.financial_products.split(',')
            financial_products.append(financial_product)
            if len(financial_products) > 1:
                financial_products = ','.join(financial_products)
            user_field(user, "financial_products", financial_products)

        if 'password1' in data:
            user.set_password(data['password1'])
        else:
            user.set_unusable_password()

        self.populate_username(request, user)

        if commit:
            user.save()

        return user