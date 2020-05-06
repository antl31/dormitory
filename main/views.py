from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.template import loader
from weasyprint import HTML
from django.template.loader import get_template
from django.http import HttpResponse

from .serializers import RoomSerializer, CustomUserSerializer
from .models import Room, CustomUser
from dormitory.celery import send_email_room


class RoomViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """ View class for work with Rooms."""

    permission_classes = [permissions.IsAuthenticated]
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get(self, request):
        serializer = RoomSerializer(self.request)
        data = serializer.data
        return Response(data)


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """ View class for work with Users."""

    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get(self, request):
        serializer = CustomUserSerializer(self.request.user)
        data = serializer.data
        return Response(data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.room:
            old_room_number = instance.room.id
        else:
            old_room_number = -1
        serializer = CustomUserSerializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            if request.data.get('room'):
                if request.data['room'] == old_room_number:
                    return Response(serializer.data)
                elif request.data['room'] != old_room_number and old_room_number != -1:
                    new_room_id = request.data['room']
                    new_room = Room.change_quanity_room(new_room_id, old_room_number)
                    send_email_room.delay(email=instance.email, room=new_room.number)
                else:
                    room_id = request.data['room']
                    new_room = Room.add_user_to_room(room_id)
                    send_email_room.delay(email=instance.email, room=new_room.number)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


def pdf_template_statistics(request):
    user = CustomUser.objects.order_by('last_name', 'first_name')
    template = loader.get_template('adminka.html')
    context = {
        'user': user,
        'num': ''
    }
    html = template.render(context)

    pdf_file = HTML(string=html).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="full list.pdf"'
    return response


def blank_a4(request, user_id):
    user = CustomUser.objects.get(id=user_id)

    context = {'full_name_dekan': '',
               'facultet': "",
               "reason_first_part": '',
               'full_name': f'{user.first_name} {user.last_name}',
               'room': user.room.number if user.room else '',
               'num': '',
               }
    template = get_template('blank_a4.html')
    html = template.render(context)

    pdf_file = HTML(string=html).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="blank_a4.pdf"'
    return response


def blank_a5(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    context = {'full_name': f'{user.last_name} {user.first_name}',
               'room': user.room.number if user.room else '',
               'group': user.group if user.group else ''
               }
    template = get_template('blank_a5.html')
    html = template.render(context)

    pdf_file = HTML(string=html).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="blank_a5.pdf"'
    return response
