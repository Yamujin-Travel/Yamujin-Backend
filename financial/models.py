from django.db import models
from django.conf import settings

class Deposit(models.Model):
    name = models.CharField(max_length=100)
    deposit_code = models.CharField(max_length=100)  # 금융상품 코드
    dcls_month = models.CharField(max_length=20)  # 공시 제출월 [YYYYMM]
    fin_co_no = models.CharField(max_length=100)  # 금융회사 코드
    kor_co_nm = models.CharField(max_length=100)  # 금융회사 명
    join_way = models.CharField(max_length=100)  # 가입 방법
    mtrt_int = models.TextField(blank=True, null=True)  # 만기 후 이자율
    spcl_cnd = models.TextField(blank=True, null=True)  # 우대조건
    join_deny = models.IntegerField(blank=True, null=True)  # 가입제한 (Ex) 1:제한없음, 2:서민전용, 3:일부제한
    join_member = models.TextField(blank=True, null=True)  # 가입대상
    etc_note = models.TextField(blank=True, null=True)  # 기타 유의사항
    max_limit = models.IntegerField(blank=True, null=True)  # 최고한도

    contract_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='contract_deposit')  # 계약 사용자

class Saving(models.Model):
    name = models.CharField(max_length=100)
    saving_code = models.CharField(max_length=100)  # 금융상품 코드
    dcls_month = models.CharField(max_length=20)  # 공시 제출월 [YYYYMM]
    fin_co_no = models.CharField(max_length=100)  # 금융회사 코드
    kor_co_nm = models.CharField(max_length=100)  # 금융회사 명
    join_way = models.CharField(max_length=100)  # 가입 방법
    mtrt_int = models.TextField(blank=True, null=True)  # 만기 후 이자율
    spcl_cnd = models.TextField(blank=True, null=True)  # 우대조건
    join_deny = models.IntegerField(blank=True, null=True)  # 가입제한 (Ex) 1:제한없음, 2:서민전용, 3:일부제한
    join_member = models.TextField(blank=True, null=True)  # 가입대상
    etc_note = models.TextField(blank=True, null=True)  # 기타 유의사항
    max_limit = models.IntegerField(blank=True, null=True)  # 최고한도

    contract_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='contract_saving')  # 계약 사용자

class DepositOption(models.Model):
    deposit = models.ForeignKey(Deposit, on_delete=models.CASCADE)
    intr_rate_type_nm = models.CharField(max_length=2)  # 저축 금리 유형명
    save_trm = models.CharField(max_length=3)  # 저축 기간 [단위: 개월]
    intr_rate = models.FloatField(null=True)  # 저축 금리 [소수점 2자리]
    intr_rate2 = models.FloatField(null=True)  # 최고 우대금리 [소수점 2자리]

class SavingOption(models.Model):
    saving = models.ForeignKey(Saving, on_delete=models.CASCADE)  
    intr_rate_type_nm = models.CharField(max_length=2)  # 저축 금리 유형명
    rsrv_type_nm = models.CharField(max_length=10)  # 적립 유형명
    save_trm = models.CharField(max_length=3)  # 저축 기간 [단위: 개월]
    intr_rate = models.FloatField(null=True)  # 저축 금리 [소수점 2자리]
    intr_rate2 = models.FloatField(null=True)  # 최고 우대금리 [소수점 2자리]
