from rest_framework import serializers

from .models import LopHoc, SinhVien, AnhDangKy, ChiTietLopHoc

class SinhVienSerializer(serializers.ModelSerializer):
    class Meta:
        model = SinhVien
        fields = '__all__'
    
    # def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        # return SinhVien.objects.create(**validated_data)

class AnhDangKySerializer(serializers.ModelSerializer):
    class Meta:
        model = AnhDangKy
        fields = '__all__'

class ChiTietLopHocSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChiTietLopHoc
        fields = '__all__'
    
class LopHocSerializer(serializers.ModelSerializer):
    class Meta:
        model = LopHoc
        fields = '__all__'