from rest_framework import viewsets
from .models import Product, Contact
from .serializers import ProductSerializer, ContactSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)  # Detect if it's a PATCH request (partial update)
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data, partial=partial)  # Pass the 'partial' flag
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        product = self.get_object()
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ContactView(APIView):
    def post(self, request):
        logger.info("Contact form hit!")
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Your message has been sent successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

class ProductRatingView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def patch(self, request, product_id):
        rating = request.data.get('rating')

        if rating is None:
            return Response({"message": "Rating not provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            rating = int(rating)  # Ensure the rating is an integer
            if rating < 0 or rating > 5:  # Assuming a 1-5 rating system
                return Response({"message": "Rating must be between 1 and 5"}, status=status.HTTP_400_BAD_REQUEST)

            product = Product.objects.get(id=product_id)
            product.ratings = rating
            product.save()
            return Response({"message": "Rating updated successfully"}, status=status.HTTP_200_OK)
        except ValueError:
            return Response({"message": "Invalid rating value"}, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)