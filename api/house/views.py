from rest_framework import generics
from .models import House
from .serializers import HouseSerializer
from joblib import load
from rest_framework.response import Response
from rest_framework import status

model = load('../house_price_prediction_xgb_model.joblib')


class HouseList(generics.ListCreateAPIView):
    queryset = House.objects.all()
    serializer_class = HouseSerializer

    def perform_create(self, serializer):
        house = serializer.save()
        house.predict_house_price()
        house.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        instance = serializer.instance

        price = int(instance.ev_fiyati)

        house_info = {
            "ilce": instance.get_ilce_display(),
            "kullanım_durumu": instance.get_kullanım_durumu_display(),
            "bulundugu_kat": instance.get_bulundugu_kat_display(),
            "bina_yasi": instance.get_bina_yasi_display(),
            "turu": instance.get_turu_display(),
            "oda_sayisi": instance.get_oda_sayisi_display(),
            "sehir": instance.get_sehir_display(),
            "mahalle": instance.get_mahalle_display(),
            "isitma_tipi": instance.get_isitma_tipi_display(),
            "bina_kat_sayisi": instance.bina_kat_sayisi,
            "net_metrekare": instance.net_metrekare,
            "price_house": price,
        }

        return Response(house_info, status=status.HTTP_201_CREATED, headers=headers)
