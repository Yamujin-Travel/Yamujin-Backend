from rest_framework import serializers
from allauth.account.adapter import get_adapter
from .models import User
from dj_rest_auth.registration.serializers import RegisterSerializer
from financial.serializers import ContractDepositSerializer, ContractSavingSerializer

class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(max_length=100)
    nickname = serializers.CharField(max_length=100)
    email = serializers.EmailField()
   
    def get_cleaned_data(self):
        return {
            'username': self.validated_data['username'],
            'password1': self.validated_data['password1'],
            'password2': self.validated_data['password2'],
            'nickname': self.validated_data['nickname'],
            'email': self.validated_data['email'],
        }
    
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'email', 'profile_img',)
        read_only_fields = ('id','username',)


class UserInfoSerializer(serializers.ModelSerializer):
        profile_img = serializers.ImageField(use_url=True)
        contract_deposit = ContractDepositSerializer(many=True)
        contract_saving = ContractSavingSerializer(many=True)
        class Meta:
            model = User
            fields = '__all__'
            read_only_fields = ('id','username',)




