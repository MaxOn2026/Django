from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [SearchFilter]

    def get_queryset(self):
        queryset = Stock.objects.all().prefetch_related('positions', 'positions__product')
        search = self.request.query_params.get('search')
        products = self.request.query_params.get('products')

        if products:
            queryset = queryset.filter(positions__product_id=products).distinct()

        if search:
            queryset = queryset.filter(
                positions__product__title__icontains=search
            ) | queryset.filter(
                positions__product__description__icontains=search
            )
            queryset = queryset.distinct()

        return queryset
