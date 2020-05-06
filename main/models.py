from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class Hostel(models.Model):
    number_hostel = models.SmallIntegerField()
    address = models.CharField(max_length=50)
    quantity_mest = models.IntegerField()

    def __str__(self):
        return 'Hostel №{}'.format(self.number_hostel)


class Room(models.Model):
    number = models.IntegerField(unique=True)
    floor = models.SmallIntegerField(blank=True)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    max_quantity = models.SmallIntegerField(blank=True)
    now_quantity = models.SmallIntegerField(blank=True)

    def __str__(self):
        return '{} - {}'.format(self.number, self.hostel)

    @staticmethod
    def change_quanity_room(new_room_id, old_room_id):
        new_room = Room.objects.get(id=new_room_id)
        old_room = Room.objects.get(id=old_room_id)

        old_room.now_quantity = - 1
        new_room.now_quantity = + 1
        new_room.save()
        old_room.save()
        return new_room

    @staticmethod
    def add_user_to_room(room_id):
        new_room = Room.objects.get(id=room_id)
        new_room.now_quantity = new_room.now_quantity + 1
        new_room.save()
        return new_room


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    course = models.SmallIntegerField(blank=True, null=True)
    group = models.CharField(max_length=12, blank=True)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField(unique=True, null=False, blank=False)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_(
                                        'Designates whether this user should be treated as active.'
                                        ' ''Unselect this instead of deleting accounts.'),
                                    )

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email
