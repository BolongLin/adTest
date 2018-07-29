from rest_framework import serializers
from goods.models import Product, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class GoodsSerializer(serializers.ModelSerializer):
    tag_list = TagSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'type_id', 'weight', 'stock', 'tags', 'tag_list',)

    def create(self, validated_data):
        instance = Product.objects.create(name=validated_data['name'], stock=validated_data['stock'],
                                          type_id=validated_data['type_id'])
        instance.price = validated_data.get('price', instance.price)
        instance.type_id = validated_data.get('type_id', instance.type_id)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.stock = validated_data.get('stock', instance.stock)
        temp = validated_data['tags'].split(',')
        map(instance.tags.add, temp)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.type_id = validated_data.get('type_id', instance.type_id)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.stock = validated_data.get('stock', instance.stock)
        instance.tags.clear()
        temp = validated_data['tags'].split(',')
        map(instance.tags.add, temp)
        instance.save()
