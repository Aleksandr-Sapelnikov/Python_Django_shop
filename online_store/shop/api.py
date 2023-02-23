from rest_framework import viewsets, status
from rest_framework.mixins import ListModelMixin, CreateModelMixin

from .models import Order
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView


class OrderAPIUpdate(APIView):

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        print('запрос пришел', pk)

        print(request.data['card_num'])
        card_num = int(request.data['card_num'].replace(' ', ''))
        last_num = int(str(card_num)[-1])
        print(card_num)
        if not pk:
            return Response({'error': 'Method PUT not allowed'})

        try:
            instance = Order.objects.get(pk=pk)
        except:
            return Response({'error': 'Object does not exists'})

        if card_num % 2 == 0 and last_num != 0:
            print('Номер оканчивается на: ', last_num, 'Значит прошел')
            serializer = OrderSerializer(instance=instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'order': serializer.data})
        else:
            print('Номер оканчивается на: ', last_num, 'ОТКАЗ')
            serializer = OrderError(instance=instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'order': serializer.data})
