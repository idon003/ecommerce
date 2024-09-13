from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import Product

from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Cart"])
class CartView(APIView):
    serializer_class = CartSerializer
    def get(self, request):
        user = request.user
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({"message": "Cart is empty"})
        serializer = CartSerializer(cart)
        return Response(serializer.data)


@extend_schema(tags=["Cart"])
class AddToCartView(APIView):
    serializer_class = CartSerializer
    def post(self, request):
        user = request.user
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=user)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data)


@extend_schema(tags=["Cart"])
class RemoveFromCartView(APIView):
    serializer_class = CartSerializer
    def post(self, request):
        user = request.user
        product_id = request.data.get("product_id")

        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response(
                {"error": "Cart does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.delete()
        except CartItem.DoesNotExist:
            pass

        serializer = CartSerializer(cart)
        return Response(serializer.data)
