from rest_framework import serializers
from .models import CustomUserModel

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUserModel
        fields = [
            'id', 'email', 'password', 'password2',
            'full_name', 'phone_number',
            'profile_image', 'role', 'address'
        ]
        read_only_fields = ['id']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        return CustomUserModel.objects.create_user(**validated_data) 




class LoginSerilizer(serializers.Serializer):
    email=serializers.CharField()        
    password=serializers.CharField(write_only=True)   


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = ['full_name','phone_number','profile_image','address']



#   python manage.py runserver