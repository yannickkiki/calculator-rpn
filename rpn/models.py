from django.db import models


class StackItemManager(models.Manager):
    def perform_operation(self, operator):
        items_for_operation = self.model.objects.order_by("-created")[:2]

        first_operand = items_for_operation[1].value
        second_operand = items_for_operation[0].value

        if operator == "+":
            operation_result = first_operand + second_operand
        elif operator == "-":
            operation_result = first_operand - second_operand
        elif operator == "*":
            operation_result = first_operand * second_operand
        elif operator == "/":
            operation_result = first_operand / second_operand
        else:
            raise NotImplementedError

        self.model.objects.filter(
            id__in=[item.id for item in items_for_operation]
        ).delete()
        self.model.objects.create(value=operation_result)


class StackItem(models.Model):
    value = models.DecimalField(max_digits=15, decimal_places=6)
    created = models.DateTimeField(auto_now_add=True)

    objects = StackItemManager()
