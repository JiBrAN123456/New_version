from rest_framework import serializers
from .models import VehicleInventory


class VehicleInventorySerializer(serializers.Serializer):
    #images = 
    
    class Meta:
         model = VehicleInventory
         fields = "__all__"
         read_only_fields =  ["company", "created_by"]


    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["company"] = user.company
        validated_data["created_by"] = user
        return VehicleInventory.objects.create(**validated_data)
    
    