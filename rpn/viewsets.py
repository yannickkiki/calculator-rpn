from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from rpn.models import StackItem
from rpn.serializers import StackItemSerializer, StackOperationSerializer


class StackItemViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = StackItemSerializer
    queryset = StackItem.objects.all()

    def get_serializer_class(self):
        if self.action == "operate":
            return StackOperationSerializer
        return StackItemSerializer

    def create(self, request, *args, **kwargs):
        """
        Add an item to the stack.
        """
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
        List items in the stack.
        """
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=["delete"])
    def clear(self, request, *args, **kwargs):
        """
        Remove all elements in the stack.
        """
        StackItem.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["post"])
    def operate(self, request, *args, **kwargs):
        """
        Perform the operation described by the "operator" parameter on the stack.\n
        Operations supported: addition ( + ), subtraction ( - ), multiplication( * ), division ( / ).
        """
        operation_serializer = StackOperationSerializer(data=request.data)
        operation_serializer.is_valid(raise_exception=True)
        operation_serializer.perform_operation()

        items_serializer = StackItemSerializer(StackItem.objects.all(), many=True)
        return Response(items_serializer.data)
