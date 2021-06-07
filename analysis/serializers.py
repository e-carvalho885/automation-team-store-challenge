from rest_framework import serializers, validators

from .models import Analysis
from .utils import (
    calculate_reynolds_number,
    get_reynolds_number_regime,
)


class AnalysisSerializer(serializers.ModelSerializer):

    reynolds_number = serializers.SerializerMethodField()
    reynolds_number_regime = serializers.SerializerMethodField()

    class Meta:
        model = Analysis
        fields = "__all__"

    def get_reynolds_number(self, obj):
        try:
            reynolds_number = calculate_reynolds_number(
                obj.diameter,
                obj.viscosity,
                obj.flow,
            )
        except ValueError:
            raise serializers.ValidationError(
                {
                    "reynolds_number": "The values you entered do not match a valid analysis."
                }
            )
        return reynolds_number

    def get_reynolds_number_regime(self, obj):
        try:
            reynolds_number = calculate_reynolds_number(
                obj.diameter,
                obj.viscosity,
                obj.flow,
            )
        except ValueError:
            raise serializers.ValidationError(
                {
                    "reynolds_number_regime": "The values you entered do not match a valid analysis."
                }
            )
        reynolds_number_regime = get_reynolds_number_regime(reynolds_number)
        return reynolds_number_regime
