from django.conf import settings
from django.db import models


class TheatreHall(models.Model):
    name = models.CharField(max_length=125, unique=True)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]


class Genre(models.Model):
    name = models.CharField(max_length=125, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]


class Actor(models.Model):
    first_name = models.CharField(max_length=125)
    last_name = models.CharField(max_length=125)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name

    class Meta:
        ordering = ["first_name"]


class Play(models.Model):
    title = models.CharField(max_length=125)
    description = models.TextField()
    genres = models.ManyToManyField(Genre, blank=True, related_name="plays")
    actors = models.ManyToManyField(Actor, blank=True, related_name="plays")

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ["title"]


class Performance(models.Model):
    play = models.ForeignKey(
        Play, on_delete=models.CASCADE, related_name="performances"
    )
    theatre_hall = models.ForeignKey(
        TheatreHall, on_delete=models.CASCADE, related_name="performances"
    )
    show_time = models.DateTimeField()

    def __str__(self) -> str:
        return self.play.title + " " + str(self.show_time)

    class Meta:
        ordering = ["-show_time"]


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return str(self.created_at)

    class Meta:
        ordering = ["-created_at"]


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    performance = models.ForeignKey(
        Performance, on_delete=models.CASCADE, related_name="tickets"
    )
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name="tickets"
    )

    def __str__(self) -> str:
        return (
            f"{str(self.performance)} (row: {self.row}, seat: {self.seat})"
        )

    class Meta:
        unique_together = ("performance", "row", "seat")
        ordering = ["row", "seat"]
