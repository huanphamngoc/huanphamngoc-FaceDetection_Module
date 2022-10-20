from django.db import models
import uuid
# Create your models here.


class TaiKhoan(models.Model):
    magv = models.CharField(primary_key=True, max_length=10)
    mat_khau = models.CharField(max_length=20, null=False)
    ho_ten = models.CharField(max_length=50, null=False, blank=False)
    nam_sinh = models.DateField(null=True)
    so_dien_thoai = models.CharField(max_length=10, null=True)


class LichSuDangNhap(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    thoi_gian = models.DateTimeField(auto_now=True, null=True)
    tai_khoan = models.ForeignKey(TaiKhoan, on_delete=models.CASCADE)
    
