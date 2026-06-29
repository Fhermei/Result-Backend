from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Extends the default JWT serializer to also accept matric_no login for students.
    Payload can be:
      { "email": "...", "password": "..." }
    OR
      { "matric_no": "...", "password": "..." }
    """

    # Override the default username field to be optional
    username_field = User.USERNAME_FIELD  # This is 'email' in your case
    
    # Make email optional by not requiring it
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make email field optional
        self.fields['email'] = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
        # Add matric_no field
        self.fields['matric_no'] = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=50)
        # Password is already required

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        token['full_name'] = user.get_full_name()
        token['email'] = user.email
        return token

    def validate(self, attrs):
        # Get values from attrs
        email = attrs.get('email', '').strip() if attrs.get('email') else ''
        matric_no = attrs.get('matric_no', '').strip() if attrs.get('matric_no') else ''
        password = attrs.get('password', '')

        print(f"Login attempt - email: '{email}', matric_no: '{matric_no}'")

        # Must provide either email or matric_no
        if not email and not matric_no:
            raise serializers.ValidationError(
                {'detail': 'Please provide either an email address or matric number.'}
            )

        # If matric_no is provided, find the associated student
        if matric_no and not email:
            try:
                from apps.students.models import StudentProfile
                # Try exact match first (case insensitive)
                student = StudentProfile.objects.filter(
                    matric_no__iexact=matric_no
                ).select_related('user').first()
                
                if student:
                    email = student.user.email
                    print(f"Found student via matric exact: {student.matric_no} -> {email}")
                else:
                    # Try contains match
                    student = StudentProfile.objects.filter(
                        matric_no__icontains=matric_no
                    ).select_related('user').first()
                    
                    if student:
                        email = student.user.email
                        print(f"Found student via contains: {student.matric_no} -> {email}")
                    else:
                        raise serializers.ValidationError(
                            {'detail': f'No student found with matric number "{matric_no}".'}
                        )
            except Exception as e:
                print(f"Error finding student: {e}")
                raise serializers.ValidationError(
                    {'detail': f'Error finding student: {str(e)}'}
                )

        # If we don't have email by now, something went wrong
        if not email:
            raise serializers.ValidationError(
                {'detail': 'Could not find a user with the provided credentials.'}
            )

        # Authenticate with email + password
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )

        if not user:
            raise serializers.ValidationError(
                {'detail': 'Invalid credentials. Please check your password and try again.'}
            )

        if not user.is_active:
            raise serializers.ValidationError(
                {'detail': 'This account has been deactivated. Contact the administrator.'}
            )

        self.user = user

        refresh = self.get_token(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'role': user.role,
            'full_name': user.get_full_name(),
            'email': user.email,
            'user_id': user.id,
        }
        return data


class UserListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'role', 'is_active']

    def get_full_name(self, obj):
        return obj.get_full_name()


class UserDetailSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'role', 'phone', 'avatar', 'is_active', 'date_joined',
        ]
        read_only_fields = ['id', 'date_joined']

    def get_full_name(self, obj):
        return obj.get_full_name()


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'role', 'phone', 'password', 'password2']

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                f'A user with the email "{value}" already exists. '
                'Please use a different email address.'
            )
        return value.lower()

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({'new_password': 'Passwords do not match.'})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect.')
        return value