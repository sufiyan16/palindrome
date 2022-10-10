from users.models import Profile
from rest_framework import serializers
from palindrome.models import Palindrome
from users.models import Profile, User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator


class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Profile
        fields='__all__'

class PalindromeSerializer(serializers.ModelSerializer):
    owner=ProfileSerializer(many=False)
    class Meta:
        model=Palindrome
        fields='__all__'

class CreatePalindromeSerializer(serializers.ModelSerializer):  

    class Meta:
        model=Palindrome
        fields='__all__'

class RegisterSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(
    required=True,
    validators=[UniqueValidator(queryset=User.objects.all())]
  )
  password = serializers.CharField(
    write_only=True, required=True, validators=[validate_password])
  password2 = serializers.CharField(write_only=True, required=True)
  class Meta:
    model = User
    fields = ('username', 'password', 'password2',
         'email', 'first_name', 'last_name')
    extra_kwargs = {
      'first_name': {'required': True},
      'last_name': {'required': True}
    }
  def validate(self, attrs):
    if attrs['password'] != attrs['password2']:
      raise serializers.ValidationError(
        {"password": "Password fields didn't match."})
    return attrs
  def create(self, validated_data):
    user = User.objects.create(
      username=validated_data['username'],
      email=validated_data['email'],
      first_name=validated_data['first_name'],
      last_name=validated_data['last_name']
    )
    user.set_password(validated_data['password'])
    user.save()
    return user


class UpdateUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = ['name', 'email', 'username',
                  ]
    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']

        instance.save()