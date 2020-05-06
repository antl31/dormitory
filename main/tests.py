from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from main.serializers import RoomSerializer, CustomUserSerializer
from main.models import Hostel, Room, CustomUser


class HostelTestCase(TestCase):
    def setUp(self):
        self.hostel1 = Hostel.objects.create(number_hostel=1, address="Street #1", quantity_mest=100)
        self.hostel2 = Hostel.objects.create(number_hostel=2, address="Street #2", quantity_mest=150)
        self.hostel3 = Hostel.objects.create(number_hostel=3, address="Street #3", quantity_mest=200)

    def test_create_hostel(self):
        self.assertEqual(self.hostel1.__str__(), "Hostel №1")
        self.assertEqual(self.hostel2.__str__(), "Hostel №2")
        self.assertEqual(self.hostel3.__str__(), "Hostel №3")
        self.assertEqual(self.hostel1.number_hostel, 1)
        self.assertEqual(self.hostel1.address, "Street #1")
        self.assertEqual(self.hostel1.quantity_mest, 100)
        self.assertEqual(Hostel.objects.count(), 3)

    def test_delete_object(self):
        self.hostel1.delete()
        self.assertEqual(Hostel.objects.count(), 2)


class RoomTestCase(TestCase):
    def setUp(self):
        self.hostel1 = Hostel.objects.create(number_hostel=1, address="Street #1", quantity_mest=100)
        self.room1 = Room.objects.create(number=100, floor=1, hostel=self.hostel1, max_quantity=3, now_quantity=0)
        self.room2 = Room.objects.create(number=101, floor=1, hostel=self.hostel1, max_quantity=2, now_quantity=0)

    def test_create_room(self):
        self.assertEqual(self.room1.__str__(), "100 - Hostel №1")
        self.assertEqual(self.room1.number, 100)
        self.assertEqual(self.room1.floor, 1)
        self.assertEqual(self.room1.max_quantity, 3)
        self.assertEqual(self.room1.now_quantity, 0)
        self.assertEqual(Room.objects.count(), 2)

    def test_delete_room(self):
        self.room1.delete()
        self.assertEqual(Room.objects.count(), 1)


class TestCustomUser(TestCase):
    def setUp(self) -> None:
        self.hostel1 = Hostel.objects.create(number_hostel=1, address="Street #1", quantity_mest=100)
        self.room1 = Room.objects.create(number=100, floor=1, hostel=self.hostel1, max_quantity=3, now_quantity=0)
        self.user = CustomUser.objects.create(first_name="name", last_name="last", course=4, group="123",
                                              hostel=self.hostel1, room=self.room1, email="123@adm.com")
        self.user2 = CustomUser.objects.create(first_name="name", last_name="last", course=4, group="123",
                                               hostel=self.hostel1, room=self.room1, email="new_adm@adm.com")

    def test_create_user(self):
        self.assertEqual(CustomUser.objects.count(), 2)
        self.assertEqual(self.user.first_name, "name")
        self.assertEqual(self.user2.__str__(), "new_adm@adm.com")

    def test_delete_hostel(self):
        self.user.delete()
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_get_name(self):
        self.assertEqual(self.user2.get_full_name(), "new_adm@adm.com")
        self.assertEqual(self.user2.get_short_name(), "name")


class TestSerialier(APITestCase):
    def test_roomserializer(self):
        self.data = {'now_quantity': 1, "max_quantity": 2}
        self.new_ser = RoomSerializer.validate(self, self.data)
        self.assertEqual(self.new_ser, self.data)

    def test_prof_serializer(self):
        self.data = {'email': "adm", "first_name": "First_name", "last_name": "last_name"}
        self.new_ser = CustomUserSerializer.validate(self, self.data)
        self.assertEqual(self.new_ser, self.data)


class TestAPIViews(TestCase):
    url = reverse("room-list")

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(email='testuser@test.com', password='testing')
        self.user.save()
        token = Token.objects.create(user=self.user)
        token.save()

    def _require_login(self):
        self.client.login(username='testuser', password='testing')

    def test_ListAccounts_authenticated(self):
        self._require_login()
        request = self.client.get(self.url)
        print(self.user.is_authenticated)

        self.assertEqual(request.status_code, 401)
