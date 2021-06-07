from django.db import models
from django.core.exceptions import ValidationError
from math import pi, log10
from scipy import constants
from django.conf import settings


class Analysis(models.Model):
    def validate_positive_float(value):
        if value <= 0.0:
            raise ValidationError(
                ("%(value)s must be in greater than 0."),
                params={"value": value},
            )

    viscosity = models.FloatField(
        "viscosity",
        validators=[validate_positive_float],
        help_text="Kinematic Viscosity in St",
    )
    diameter = models.FloatField(
        "diameter", validators=[validate_positive_float], help_text="Pipe Diameter in m"
    )
    flow = models.FloatField(
        "flow",
        validators=[validate_positive_float],
        help_text="Fluid flow in the pipe in m³/s",
    )

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=1,
        verbose_name="Creator",
    )

    def __str__(self):
        return f"viscosity = {self.viscosity} | diameter = {self.diameter} | flow = {self.flow}"

    class Meta:
        verbose_name_plural = "Analyses"
