from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from django.conf import settings
from .models import CustomUser, UserRole


# ---------------------
# Register Serializer
# ---------------------
class CustomRegisterSerializer(RegisterSerializer):
    username = None  # Remove username

    # Common fields
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    name = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
    profile_picture = serializers.ImageField(required=False, allow_null=True)

    # Conditional role field
    if getattr(settings, "USE_ROLE", False):
        role = serializers.ChoiceField(choices=UserRole.choices, required=True)

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "password",
            "name",
            "phone_number",
            "profile_picture",
        ) + (("role",) if getattr(settings, "USE_ROLE", False) else ())

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data["email"] = self.validated_data.get("email", "")
        data["name"] = self.validated_data.get("name", "")
        data["phone_number"] = self.validated_data.get("phone_number", "")
        data["profile_picture"] = self.validated_data.get("profile_picture", None)

        if getattr(settings, "USE_ROLE", False):
            data["role"] = self.validated_data.get("role", UserRole.USER)

        return data

    def save(self, request):
        user = CustomUser.objects.create(
            email=self.validated_data["email"],
            name=self.validated_data.get("name", ""),
            phone_number=self.validated_data.get("phone_number", ""),
            profile_picture=self.validated_data.get("profile_picture", None),
            role=self.validated_data.get("role", UserRole.USER)
            if getattr(settings, "USE_ROLE", False)
            else UserRole.USER,
        )
        user.set_password(self.validated_data["password"])
        user.save()
        return user


# ---------------------
# Login Serializer
# ---------------------
class CustomLoginSerializer(LoginSerializer):
    username = None  # remove username completely
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(self.context['request'], email=email, password=password)
            if not user:
                raise serializers.ValidationError(
                    _('Unable to log in with provided credentials.'),
                    code='authorization'
                )
        else:
            raise serializers.ValidationError(
                _('Must include "email" and "password".'),
                code='authorization'
            )

        attrs['user'] = user
        return attrs


# ---------------------
# User Response Serializer
# ---------------------
class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'name',
            'phone_number',
            'profile_picture',
            'role',
        ]
        read_only_fields = fields

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not getattr(settings, 'USE_ROLE', False):
            data.pop('role', None)
        return data
