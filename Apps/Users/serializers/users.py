from rest_framework import serializers

from django.contrib.auth import get_user_model

User = get_user_model()


class UserOnlySerializer(serializers.ModelSerializer):
    """
    This Serializer is only for user creation and user to see his own data,
    This serializer may not be used for public data transfer
    """
    class Meta:
        model = User
        fields = ['id',
                  'username',
                  'password',
                  'email',
                  'first_name',
                  'last_name',
                  'phone_number',
                  'phone_number_ccode',
                  'date_of_birth'
                  ]
        extra_kwargs = {
            "password": {
                'write_only': True
            }
        }

    def create(self, validated_data):
        # Get Password
        password = validated_data.get('password', None)
        # Init Instance
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance


class UserRetrieveSerializer(serializers.ModelSerializer):
    """
    This serializer will be used for public data transfer
    """
    name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', "username", 'name'
        ]

    @staticmethod
    def get_name(obj: User):
        return obj.name
