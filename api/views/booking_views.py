from ..serializers.booking_serializer import (
  BookingSerializer,
  Booking,
  BookingPaymentSerializer,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.bankist_serializer import BankistSerializer,Bankist,TransactionHistory
from rest_framework import viewsets,status
from users.models import User
class BookingApiView(viewsets.ModelViewSet):
  queryset = Booking.objects.all()
  serializer_class = BookingSerializer
  
  
  
class BookingPaymentApiView(APIView):
  COMPANY_BANK_ACCOUNT_NUMBER = 50003442236121 
  COMPANY_NAME = 'vist ethiopia'

  def post(self,request):
    current_user_bookings = Booking.objects.filter(user=request.user)
    if not current_user_bookings.exists():
        return Response({"error": "User doesn't have any bookings."}, status=status.HTTP_404_NOT_FOUND)
    pending_user_bookings = current_user_bookings.filter(status=Booking.Status.PENDING)
    if not pending_user_bookings.exists():
      return Response({"message": "All user bookings are confirmed."}, status=status.HTTP_204_NO_CONTENT)

    
    serializer = BookingPaymentSerializer(data = request.data)
    if serializer.is_valid():
      
      package_name = serializer.validated_data['package_name'] 
      pin = serializer.validated_data['pin']
      
      current_booking_package = pending_user_bookings.filter(package__package_name=package_name).first()
      if not current_booking_package:
        return Response({"error": "Booking for the specified package not found or not pending."}, status=status.HTTP_404_NOT_FOUND)

      try:
        sender_bank_account = Bankist.objects.get(user_profile__user = request.user)
      except Bankist.DoesNotExist:
        return Response({"error": "You don't have a bank account. Please create one."},status=status.HTTP_404_NOT_FOUND)
      price = current_booking_package.total_price
      company_name = 'vist ethiopia'
      reciver_bank_account = Bankist.objects.get(account_number= self.COMPANY_BANK_ACCOUNT_NUMBER)
      
      
            
            # Validate PIN
      if not sender_bank_account.check_pin(pin):
          return Response(
              {"message": "PIN doesn't match. Please try again!"},
              status=status.HTTP_403_FORBIDDEN
          )

      # Check for sufficient balance
      if sender_bank_account.balance < price:
        current_booking_package.status = Booking.Status.CANCELED
        current_booking_package.save()
        return Response(
              {"message": "Insufficient balance! booking canceled","balance":f"your balance is {sender_bank_account.balance}","total_price_needed":current_booking_package.total_price},
              status=status.HTTP_400_BAD_REQUEST
          )

      # Perform withdrawal
      sender_bank_account.balance -= price
      reciver_bank_account.balance += price
      sender_transaction = TransactionHistory.objects.create(
          bank_account = sender_bank_account,
          amount = -price,
          transaction_type = TransactionHistory.Status.TRANSFER
          
      )
      
      receiver_transaction = TransactionHistory.objects.create(
          bank_account = reciver_bank_account,
          amount = price,
          transaction_type = TransactionHistory.Status.TRANSFER
          
      )
      
      sender_transaction.related_transaction = receiver_transaction
      current_booking_package.status = Booking.Status.CONFIRMED
      current_booking_package.save()
      sender_transaction.save()
      sender_bank_account.save()
      reciver_bank_account.save()
      return Response({
          "message": "Transaction successful",
          "balance": f"Your  '{package_name}' booking is confirmed ",
          "receiver": f"Money successfully sent to {self.COMPANY_NAME}"}, 
          status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

