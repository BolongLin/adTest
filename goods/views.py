# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from goods.models import Product, Tag
from goods.serializer import GoodsSerializer, TagSerializer
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView


class Acquire(APIView):

    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def get(self, request):
        get = request.GET
        try:
            if get.get('id'):
                a = get.get('id')
                temp = Product.objects.get(id=a)
                return Response(GoodsSerializer(temp).data)
            else:
                type_id = get.get('type_id')
                count_pp = get.get('count_pp')
                page = get.get('page')
                temp = Product.objects.filter(type_id=type_id)
                return Response({'product': [GoodsSerializer(j).data for j in temp]})
        except ValueError:
            return Response('Illegal Input')
        except ObjectDoesNotExist:
            return Response({'result': 404})

    def post(self, request):
        post = GoodsSerializer(data=request.data)
        if post.is_valid():
            try:
                temp = Product.objects.get(name=post.data["name"])
                return Response('existed!')
            except ObjectDoesNotExist:
                p = GoodsSerializer.create(post, request.data)
                return Response({'id': p.id})
        else:
            return Response({'result': 404})

    def put(self, request):
        get = request.GET
        if get.get('id'):
            try:
                p = Product.objects.get(id=request.GET['id'])
                serializer = GoodsSerializer(data=request.data)
                if serializer.is_valid():
                    GoodsSerializer.update(serializer, p, request.data)
                    return Response({'result': 200})
                return Response(serializer.errors)
            except ValueError:
                return Response('Illegal Input')
            except ObjectDoesNotExist:
                return Response({'result': 404})
        return Response('please input an id')

    def delete(self, request):
        get = request.GET
        id = get.get('id')
        try:
            temp = Product.objects.get(id=id)
            temp.delete()
            return Response({'result': 200})
        except ValueError:
            return Response('Illegal Input')
        except ObjectDoesNotExist:
            return Response({'result': 404})
