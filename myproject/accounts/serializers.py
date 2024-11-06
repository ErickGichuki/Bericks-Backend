from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone_number', 'address', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            address=validated_data['address'],
        )
        user.set_password(validated_data['password'])

        # Set role logic (e.g., first user is admin)
        user.role = 'admin' if CustomUser.objects.count() == 0 else 'user'
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            # Attempt to get the user by email
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")

        # Check the password directly using the user instance
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password")

        attrs['user'] = user
        return attrs
