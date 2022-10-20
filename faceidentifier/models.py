from django.db import models
import uuid

from faceregister.models import ChiTietLopHoc

# Create your models here.


class DinhDanhKhuonMat(models.Model):
    ma_dinh_danh = models.UUIDField(primary_key=True,
                                    default=uuid.uuid4,
                                    editable=False)
    duong_dan_anh = models.CharField(max_length=1024, null=True)
    thoi_gian = models.DateTimeField(auto_now=True, null=True)
    status = models.BooleanField(null=True)
    chitietlophoc = models.ForeignKey(ChiTietLopHoc, on_delete=models.CASCADE)
    


class DinhDanhThuCong(models.Model):
    ma_dinh_danh = models.UUIDField(primary_key=True,
                                    default=uuid.uuid4,
                                    editable=False)
    thoi_gian = models.DateTimeField(auto_now=True, null=True)
    chitietlophoc = models.ForeignKey(ChiTietLopHoc, on_delete=models.CASCADE)