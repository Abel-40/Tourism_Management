from django.db import models
from users.models import UserProfile
from django.contrib.auth.hashers import check_password, make_password
import uuid
# Create your models here.
def account_num_genrator():
    return str(uuid.uuid4().int)[:10]

class Bankist(models.Model):
  account_number = models.CharField(unique=True,max_length=14,editable=False)
  user_profile = models.OneToOneField(UserProfile,related_name='bank_account',on_delete=models.CASCADE)
  balance = models.DecimalField(max_digits=10,decimal_places=2)
  pin = models.CharField(max_length=128)
  
  objects = models.Manager()

  def save(self,*args, **kwargs):
    
    if not self.pin.startswith('pbkdf2_sha256$'):
      self.pin = make_password(self.pin)
    if self.balance < 0:
      raise ValueError("Balance cannot be negative")
    if not self.account_number:
      self.account_number = f"5000{account_num_genrator()}"
      
    super().save(*args, **kwargs)
    
    
  def set_pin(self,raw_pin):
    self.pin = make_password(raw_pin)
  
  def check_pin(self, raw_pin):
    return check_password(raw_pin,self.pin)
  
  def __str__(self):
    return f"{self.user_profile.user.username} bank account"
  
  
class TransactionHistory(models.Model):
  class Status(models.TextChoices):
    WITHDRAWAl = "Withdrawal","WITHDRAWAl"
    DEPOSIT = "Deposit","Deposit"
    TRANSFER = "Transfer","Transfer"
    
  bank_account = models.ForeignKey(Bankist,on_delete=models.CASCADE,related_name="transaction_history")
  amount = models.DecimalField(max_digits=10,decimal_places=2)
  transaction_date = models.DateTimeField(auto_now_add=True)
  transaction_type = models.CharField(max_length=10,choices=Status.choices)
  related_transaction = models.OneToOneField('self',on_delete=models.SET_NULL,null=True,related_name = 'paired_transaction')
  def __str__(self):
    return f"{self.bank_account.user_profile.user.username} - {self.transaction_type} - {self.amount} on {self.transaction_date}"