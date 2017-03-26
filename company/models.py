from django.db import models
from django.utils.translation import ugettext_lazy as _


class Company(models.Model):
    name = models.CharField(verbose_name=_('Name'), unique=True, max_length=10)

