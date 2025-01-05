from ..serializers.booking_serializer import (
  BookingSerializer,
  Booking,
  BookingPaymentSerializer,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.bankist_serializer import BankistSerializer,Bankist,TransactionHistory
from rest_framework import viewsets,status
from packages.models import Packages
from datetime import timedelta
from django.utils import timezone
class BookingApiView(viewsets.ModelViewSet):
  queryset = Booking.objects.all()
  serializer_class = BookingSerializer
  lookup_field = 'slug'
  
  
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
      
      pakcage = Packages.objects.get(package_name=package_name)
      pakcage_start_date = pakcage.start_date
      current_date = timezone.now().date()
      if pakcage_start_date < current_date:
        current_booking_package.status = Booking.Status.CANCELED
        current_booking_package.save()
        return Response(
              {"message": "package start date passed you can't pay for this package"},
              status=status.HTTP_400_BAD_REQUEST
          )
      
      price = current_booking_package.total_price
      reciver_bank_account = Bankist.objects.get(account_number= self.COMPANY_BANK_ACCOUNT_NUMBER)
      
      
            
            # Validate PIN
      if not sender_bank_account.check_pin(pin):
          return Response(
              {"message": "PIN doesn't match. Please try again!"},
              status=status.HTTP_403_FORBIDDEN
          )

      # Check for sufficient balance
      if sender_bank_account.balance < price:
        current_booking_package.status = Booking.Status.PENDING
        current_booking_package.save()
        return Response(
              {"message": "Insufficient balance! your booking is pended. please try again!!","balance":f"your balance is {sender_bank_account.balance}","total_price_needed":current_booking_package.total_price},
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



class BookingPackageApiView(APIView):
  def post(self,request):
    current_user_bookings = Booking.objects.filter(user=request.user)
    serializer = BookingSerializer(data=request.data)
        
    if serializer.is_valid():
      package = serializer.validated_data['package']
      user = request.user
      package_name = package.package_name
      new_package_start_date = package.start_date
      if Booking.objects.filter(user=user,package=package).exists():
        return Response({"message":"You have already booked this package!"},status=status.HTTP_400_BAD_REQUEST)
      if current_user_bookings.exists():
        last_booked_package = current_user_bookings.last()
        package_start_date = last_booked_package.package.start_date
        package_days_of_tour = last_booked_package.package.days_of_tour
        last_package_end_date = (package_start_date + timedelta(days=package_days_of_tour+3))#3 added to make the end of the package and the start of package differnce in 3 days
        if new_package_start_date <= last_package_end_date:
            return Response( {"error": "You cannot book a new package your existing reservation overlap with the end date of selected package"},status=status.HTTP_400_BAD_REQUEST)
        # serializer.save()
      serializer.save(user=request.user)#to make the booking for the request user
      return Response({"message": f"Successfully booked package {package_name}.","Remember":"Remember to pay for this package and wait for confirmation."},status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      