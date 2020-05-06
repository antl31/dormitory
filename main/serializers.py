from rest_framework import serializers

from .models import Room, CustomUser


class RoomSerializer(serializers.ModelSerializer):
    """    serializer for room model    """

    def validate(self, data):
        if data['now_quantity'] > data['max_quantity'] or data['now_quantity'] < 0 or data['max_quantity'] < 0:
            raise serializers.ValidationError("This room is overflow", code=422)
        return data

    class Meta:
        model = Room
        fields = ('id', 'number', 'floor', 'hostel', 'max_quantity', 'now_quantity')


class CustomUserSerializer(serializers.ModelSerializer):
    """    serializer for profile model    """

    def validate(self, data, ):
        if data.get('room'):
            room = Room.objects.get(number=data['room'].number)
            if room.now_quantity + 1 > room.max_quantity:
                raise serializers.ValidationError("Max quanity")
        if not data['email']:
            raise serializers.ValidationError("Email is required")
        if not data['first_name']:
            raise serializers.ValidationError("First name is required")
        if not data['last_name']:
            raise serializers.ValidationError("Last name is required")
        if data.get('course'):
            if data['course'] <= 0 or data['course'] > 10:
                raise serializers.ValidationError("course not be <=0 or > 10 ")
        return data

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'course', 'group', 'hostel', 'room')
