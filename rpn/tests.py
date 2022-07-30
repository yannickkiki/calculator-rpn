from django.urls import reverse

from faker import Faker

from rest_framework import status
from rest_framework.test import APITestCase

from rpn.factories import StackItemFactory
from rpn.models import StackItem


class RpnAPITestCase(APITestCase):
    def test_stack_item_creation(self):
        self.assertFalse(StackItem.objects.exists())

        data = {
            "value": Faker().pydecimal(
                left_digits=2, right_digits=2
            )  # random decimal value
        }
        response = self.client.post(reverse("stack_items-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(StackItem.objects.count(), 1)
        item = StackItem.objects.get()
        self.assertEqual(item.value, data["value"])

    def test_stack_items_listing(self):
        stack_items = [StackItemFactory() for _ in range(3)]

        response = self.client.get(reverse("stack_items-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        stack_items_data = response.json()
        self.assertEqual(len(stack_items), len(stack_items_data))

    def test_stack_items_clearing(self):
        for _ in range(3):
            StackItemFactory()

        self.assertTrue(StackItem.objects.exists())

        response = self.client.delete(reverse("stack_items-clear"))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(StackItem.objects.exists())

    def test_stack_operate_addition(self):
        self._test_stack_operate_with_two_operands(operator="+")

    def test_stack_operate_subtraction(self):
        self._test_stack_operate_with_two_operands(operator="-")

    def test_stack_operate_multiplication(self):
        self._test_stack_operate_with_two_operands(operator="*")

    def test_stack_operate_division(self):
        self._test_stack_operate_with_two_operands(operator="/")

    def test_stack_operate_addition_validation(self):
        self._test_stack_operate_with_two_operands_validation(operator="+")

    def test_stack_operate_subtraction_validation(self):
        self._test_stack_operate_with_two_operands_validation(operator="-")

    def test_stack_operate_multiplication_validation(self):
        self._test_stack_operate_with_two_operands_validation(operator="*")

    def test_stack_operate_division_validation(self):
        self._test_stack_operate_with_two_operands_validation(operator="/")

        StackItemFactory()
        StackItemFactory(value="0")
        response = self.client.post(
            reverse("stack_items-operate"), data={"operator": "/"}
        )
        # confirm operation can not be performed (because we are requesting a division by zero)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def _test_stack_operate_with_two_operands(self, operator):
        stack_items = [StackItemFactory() for _ in range(5)]

        data = {"operator": operator}
        response = self.client.post(reverse("stack_items-operate"), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_stack_values = [item.value for item in stack_items[:-2]]
        last_value = self._apply_two_operands_operation(
            operator=operator,
            first_operand=stack_items[-2].value,
            second_operand=stack_items[-1].value,
        )
        expected_stack_values.append(last_value)

        stack_values = list(
            StackItem.objects.order_by("created").values_list("value", flat=True)
        )
        self.assertEqual(
            stack_values,
            [
                round(value, 6) for value in expected_stack_values
            ],  # set to 6 decimal digits as in the API
        )

    def _test_stack_operate_with_two_operands_validation(self, operator):
        StackItemFactory()

        data = {"operator": operator}
        response = self.client.post(reverse("stack_items-operate"), data=data)
        # confirm operation can not be performed (because there is less than two items in the stack)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        StackItemFactory()
        response = self.client.post(reverse("stack_items-operate"), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @staticmethod
    def _apply_two_operands_operation(operator, first_operand, second_operand):
        if operator == "+":
            last_value = first_operand + second_operand
        elif operator == "-":
            last_value = first_operand - second_operand
        elif operator == "*":
            last_value = first_operand * second_operand
        elif operator == "/":
            last_value = first_operand / second_operand
        else:
            raise AssertionError("Operator not supported")
        return last_value
