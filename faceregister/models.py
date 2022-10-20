from django.db import models
import uuid

from signin.models import TaiKhoan
# Create your models here.


class SinhVien(models.Model):
    masv = models.CharField(primary_key=True, max_length=10)
    ho_ten = models.CharField(max_length=50, null=False, blank=False)
    nam_sinh = models.DateField(null=True)
    so_dien_thoai = models.CharField(max_length=10, null=True)
    gioi_tinh = models.BooleanField(null=True)


class AnhDangKy(models.Model):
    ma_anh = models.UUIDField(primary_key=True,
                              default=uuid.uuid4,
                              editable=False)
    duong_dan_anh = models.CharField(max_length=1024, null=False)
    sinh_vien = models.ForeignKey(SinhVien, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['sinh_vien']


class LopHoc(models.Model):
    ma_lop = models.CharField(primary_key=True, max_length=10)
    ten_lop = models.CharField(max_length=50, null=True)
    si_so = models.PositiveSmallIntegerField(null=True)
    model_path = models.CharField(max_length=255, null=True)
    giao_vien = models.ForeignKey(TaiKhoan, null=True, on_delete=models.SET_NULL)
    sinh_vien = models.ManyToManyField(SinhVien, through='CHITIETLOPHOC')


class ChiTietLopHoc(models.Model):
    sinh_vien = models.ForeignKey(SinhVien, on_delete=models.CASCADE)
    lop_hoc = models.ForeignKey(LopHoc, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['sinh_vien', 'lop_hoc'], name="chitietlophoc_unique"
            )
        ]
