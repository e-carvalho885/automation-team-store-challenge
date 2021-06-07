from celery import task
from django.core.mail import send_mail
from .models import Analysis
from django.contrib.auth.models import User


@task
def analysis_created(email_data):

    id = email_data["id"]
    reynolds_number = email_data["reynolds_number"]
    reynolds_number_regime = email_data["reynolds_number_regime"]
    viscosity = email_data["viscosity"]
    diameter = email_data["diameter"]
    flow = email_data["flow"]

    subject = f"A new analysis was created. #{id}"
    message = (
        f"An analysis has successfully created.\n\n"
        f"Kinematic Viscosity (St) -> {viscosity}\n\n"
        f"Pipe Diameter (m) -> {diameter}\n\n"
        f"Volumetric Flow Rate (m3/s) -> {flow}\n\n"
        f"Reynolds Number -> {reynolds_number}\n\n"
        f"Reynolds Number Regime -> {reynolds_number_regime}\n\n"
    )
    mail_sent = send_mail(
        subject,
        message,
        "admin@reynoldsnumbercalculator.com",
        ["notifications@reynoldsnumbercalculator.com"],
    )

    return mail_sent
