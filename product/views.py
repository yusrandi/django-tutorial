from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializer import ProductSerializer
from .models import Product


# Create your views here.
class ProductView(ViewSet):
    # GET /api/products/
    def list(self, request):
        products = Product.objects.all()
        productSerial = ProductSerializer(products, many=True)
        return Response(
            {
                "data": productSerial.data,
            }
        )

    # POST /api/products/
    def create(self, request):

        productSerial = ProductSerializer(data=request.data)
        if productSerial.is_valid():
            productSerial.save()

        return Response(
            {
                "data": productSerial.data,
            }
        )

    # PUT /api/products/<id>/
    def update(self, request, pk=None):
        product = Product.objects.get(pk=pk)
        productUpdateSerial = ProductSerializer(product, data=request.data)
        if productUpdateSerial.is_valid():
            productUpdateSerial.save()
        return Response(
            {
                "id": pk,
                "data": productUpdateSerial.data,
            }
        )

    # DELETE /api/products/<id>/
    def destroy(self, request, pk=None):
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response({"message": "product deleted successfully"})
