from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=8,write_only=True)
    password2 = serializers.CharField(required=True, min_length=8,write_only=True)
    class Meta:
        model = User
        exclude = ['groups', 'user_permissions', 'is_superuser', 'is_staff', 'is_active']

    def validate(self, attrs):
        #print(attrs, '!!!!!!')
        password2 = attrs.pop('password2')
        if password2 !=attrs['password']:
            raise serializers.ValidationError('Password didn\'t match!')
        validate_password(attrs['password'])
        return attrs

    def validate_first_name(self, value):
        if not value.istitle():
            raise serializers.ValidationError('Name must start with uppercase lettet!')
        return value

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user





class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'user_permissions', 'groups',
                   'is_superuser', 'is_staff', 'is_active')