from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Order, OrderItem
from .serializers import OrderSerializer
from cart.models import Cart

from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Orders"])
class OrderListView(APIView):
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        order_data = request.data
        order_data["user"] = request.user.id

        serializer = OrderSerializer(data=order_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Orders"])
class OrderDetailView(APIView):
    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )


@extend_schema(tags=["Orders"])
class CheckoutView(APIView):
    def post(self, request):
        cart = Cart.objects.get(user=request.user)

        order = Order.objects.create(
            user=request.user, cart=cart, total_price=cart.total_price, status="Pending"
        )

        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                subtotal=cart_item.subtotal,
            )

        cart.ordered = True
        cart.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Orders"])
class OrderHistoryView(APIView):
    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by("-created_at")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["Orders"])
class OrderTrackingView(APIView):
    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response(
                {"message": "Order not found."}, status=status.HTTP_404_NOT_FOUND
            )
