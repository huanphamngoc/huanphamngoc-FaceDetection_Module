from rest_framework import serializers

from .models import DinhDanhKhuonMat, DinhDanhThuCong, ChiTietLopHoc

class DinhDanhKhuonMatSerializer(serializers.ModelSerializer):
    class Meta:
        model = DinhDanhKhuonMat
        fields = '__all__'
class DinhDanhThuCongSerializer(serializers.ModelSerializer):
    class Meta:
        model = DinhDanhThuCong
        fields = '__all__'
class ChiTietLopHocSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChiTietLopHoc
        fields = '__all__'

