from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from phonenumber_field.formfields import PhoneNumberField


class UserProfile(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField()
    HUMAN_CHOICES = (
        ('взрослых', 'Взрослых'),
        ('детей', 'Детей')
    )
    age = models.PositiveSmallIntegerField(default=0, null=True, blank=True,
                                           validators=[MinValueValidator(18),
                                                       MaxValueValidator(100)])
    date_registered = models.DateField(auto_now=True, null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)

    human = models.CharField(max_length=18, choices=HUMAN_CHOICES, default='взрослых')

    def __str__(self):
        return f'{self.first_name}-{self.last_name}'


class Hotel(models.Model):
    name_hotel = models.CharField(max_length=32)
    description = models.TextField()
    address = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    country = models.CharField(max_length=32)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)

    def str(self):
        return f'{self.name_hotel} - {self.country}'


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_number = models.SmallIntegerField(default=0)
    capacity = models.PositiveIntegerField(default=0)
    price_per_night = models.PositiveIntegerField()
    ROOM_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
    )
    hroom = models.CharField(max_length=18, choices=ROOM_CHOICES, default='1')


    def str(self):
        return f'{self.room_number}'


class Review(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    parent_review = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    stars = models.IntegerField(choices=[(i, str(1)) for i in range(1, 6)], verbose_name="Рейтинг")
    hotel = models.ForeignKey(Hotel, related_name='reviews', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author}'

