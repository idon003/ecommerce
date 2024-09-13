from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.decorators import APIView, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions
from django.db.models import Avg
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView

from ..models import Product, Category, Review
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer

@extend_schema(tags=["Reviews"])
class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewListView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

@extend_schema(tags=["Reviews"])
class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    def put(self, request, pk):
        review = get_object_or_404(Review, pk=pk)

        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if review.user != request.user:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

@extend_schema(tags=["Products"])
class ProductListView(APIView):
    serializer_class = ProductSerializer
    def get(self, request):
        category_id = request.query_params.get("category")

        if category_id:
            products = Product.objects.filter(category_id=category_id)
        else:
            products = Product.objects.all()

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    @permission_classes([permissions.IsAdminUser])
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Products"])
class ProductDetailView(APIView):
    serializer_class = ProductSerializer
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        reviews = Review.objects.filter(product=product)
        review_serializer = ReviewSerializer(reviews, many=True)

        return Response(
            {
                "product": serializer.data,
                "reviews": review_serializer.data,
            }
        )

    def delete(self, request, pk):
        review = get_object_or_404(Product, pk=pk)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema(tags=["Category"])
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

@extend_schema(tags=["Category"])
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
