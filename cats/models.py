from django.db import models
from django.urls import reverse


class Owner(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)

    # class Meta:
    #     verbose_name = _("")
    #     verbose_name_plural = _("s")

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})


class Cat(models.Model):
    name = models.CharField(max_length=16)
    color = models.CharField(max_length=16)
    birth_year = models.IntegerField()
    owner = models.ForeignKey(
        Owner,
        on_delete=models.CASCADE,
        related_name='cats',
        # verbose_name='Хозяин'
    )

    def __str__(self):
        return self.name
