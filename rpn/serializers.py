from django.utils.translation import gettext as _

from rest_framework import serializers

from rpn.models import StackItem


class StackItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StackItem
        fields = ["id", "value", "created"]


class StackOperationSerializer(serializers.Serializer):
    operator = serializers.ChoiceField(choices=["+", "-", "*", "/"], required=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if StackItem.objects.count() < 2:
            raise serializers.ValidationError(
                _(
                    "There should be at least two items in the stack to perform this operation."
                )
            )

        if attrs["operator"] == "/":
            last_item = StackItem.objects.last()
            if last_item.value == 0:
                raise serializers.ValidationError(_("Can not perform division by 0."))

        return attrs

    def perform_operation(self):
        return StackItem.objects.perform_operation(
            operator=self.validated_data["operator"]
        )
