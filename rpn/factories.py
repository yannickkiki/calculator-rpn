import factory

from rpn.models import StackItem


class StackItemFactory(factory.django.DjangoModelFactory):
    value = factory.Faker("pydecimal", left_digits=2, right_digits=2)

    class Meta:
        model = StackItem
