from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(
        _('created date'),
        auto_now_add=True,
        db_index=True
    )
    updated_at = models.DateTimeField(
        _('updated date'),
        auto_now=True
    )

    class Meta:
        abstract = True
