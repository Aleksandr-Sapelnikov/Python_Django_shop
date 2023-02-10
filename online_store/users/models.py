from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(blank=True, null=True, max_length=10, verbose_name='Телефон',
                             help_text='Введите без +7')
    fio = models.CharField(blank=True, null=True, max_length=60, verbose_name='ФИО')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def save_or_create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        my_group = Group.objects.get(name='Buyer')
        my_group.user_set.add(instance)
    else:
        try:
            instance.profile.save()
        except ObjectDoesNotExist:
            Profile.objects.create(user=instance)
            my_group = Group.objects.get(name='Buyer')
            my_group.user_set.add(instance)

