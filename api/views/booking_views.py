from ..serializers.booking_serializer import (
  BookingSerializer,
  Booking,
  BookingPaymentSerializer,
  BookingUpdateSerializer,
  BookingDetailSerializer
)
from bookings.views import send_payment_confirmation_email
from django.shortcuts import get_object_or_404,get_list_or_404
from rest_framework.response import Response
from ..serializers.bankist_serializer import Bankist,TransactionHistory
from rest_framework import viewsets,status
from packages.models import Packages
from rest_framework.decorators import action
from datetime import timedelta
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from bookings.permissions import IsCustomer,IsBookingOwner




class BookingApiView(viewsets.ViewSet):
    COMPANY_BANK_ACCOUNT_NUMBER = 50003254599039
    COMPANY_NAME = 'Visit Ethiopia'
    lookup_field = 'slug'
    @action(detail=False, methods=['post'], permission_classes=[IsCustomer])
    def book(self, request):
        current_user_bookings = Booking.objects.filter(user=request.user)
        serializer = BookingSerializer(data=request.data)

        if serializer.is_valid():
            package = serializer.validated_data['package']
            user = request.user
            package_name = package.package_name
            new_package_start_date = package.start_date

            if Booking.objects.filter(user=user, package=package).exists():
                return Response({"message": "You have already booked this package!"}, status=status.HTTP_400_BAD_REQUEST)

            if current_user_bookings.exists():
                last_booked_package = current_user_bookings.last()
                package_start_date = last_booked_package.package.start_date
                package_days_of_tour = last_booked_package.package.days_of_tour
                last_package_end_date = package_start_date + timedelta(days=package_days_of_tour + 3)

                if new_package_start_date <= last_package_end_date:
                    return Response(
                        {"error": "Your new package overlaps with an existing reservation."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            serializer.save(user=request.user)
            return Response(
                {"message": f"Successfully booked package {package_name}.",
                 "Remember": "Remember to pay for this package and wait for confirmation."},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post'], permission_classes=[IsBookingOwner])
    def booking_payment(self, request):
        current_user_bookings = Booking.objects.filter(user=request.user)
        user_email = request.user.email
        username = request.user.username
        if not current_user_bookings.exists():
            return Response({"error": "User doesn't have any bookings."}, status=status.HTTP_404_NOT_FOUND)

        pending_user_bookings = current_user_bookings.filter(status=Booking.Status.PENDING)
        if not pending_user_bookings.exists():
            return Response({"message": "All user bookings are confirmed."}, status=status.HTTP_204_NO_CONTENT)

        serializer = BookingPaymentSerializer(data=request.data)
        if serializer.is_valid():
            package_name = serializer.validated_data['package_name']
            pin = serializer.validated_data['pin']

            current_booking_package = pending_user_bookings.filter(package__package_name=package_name).first()
            if not current_booking_package:
                return Response({"error": "Booking for the specified package not found or not pending."},status=status.HTTP_404_NOT_FOUND)

            try:
                sender_bank_account = Bankist.objects.get(user_profile__user=request.user)
            except Bankist.DoesNotExist:
                return Response({"error": "You don't have a bank account. Please create one."},status=status.HTTP_404_NOT_FOUND)

            package = Packages.objects.get(package_name=package_name)
            package_start_date = package.start_date
            current_date = timezone.now().date()

            if package_start_date < current_date:
                current_booking_package.status = Booking.Status.CANCELED
                current_booking_package.save()
                return Response(
                    {"message": "Package start date has passed. You can't pay for this package."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            price = current_booking_package.total_price
            receiver_bank_account = Bankist.objects.get(account_number=self.COMPANY_BANK_ACCOUNT_NUMBER)

            if not sender_bank_account.check_pin(pin):
                return Response(
                    {"message": "PIN doesn't match. Please try again!"},
                    status=status.HTTP_403_FORBIDDEN
                )

            if sender_bank_account.balance < price:
                current_booking_package.status = Booking.Status.PENDING
                current_booking_package.save()
                return Response(
                    {"message": "Insufficient balance! Your booking is pending. Please try again.",
                     "balance": f"Your balance is {sender_bank_account.balance}",
                     "total_price_needed": current_booking_package.total_price},
                    status=status.HTTP_400_BAD_REQUEST
                )

            sender_bank_account.balance -= price
            receiver_bank_account.balance += price

            sender_transaction = TransactionHistory.objects.create(
                bank_account=sender_bank_account,
                amount=-price,
                transaction_type=TransactionHistory.Status.TRANSFER
            )

            receiver_transaction = TransactionHistory.objects.create(
                bank_account=receiver_bank_account,
                amount=price,
                transaction_type=TransactionHistory.Status.TRANSFER
            )

            sender_transaction.related_transaction = receiver_transaction
            current_booking_package.status = Booking.Status.CONFIRMED
            if send_payment_confirmation_email(user_email, username,package_name, price, current_date):
                current_booking_package.save()
                sender_transaction.save()
                sender_bank_account.save()
                receiver_bank_account.save()
                send_payment_confirmation_email(user_email, username, package_name, price, current_date)
                return Response(
                    {"message": "Transaction successful",
                    "balance": f"Your '{package_name}' booking is confirmed.",
                    "receiver": f"Money successfully sent to {self.COMPANY_NAME}"},
                    status=status.HTTP_200_OK
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
      
    @action(detail=True, methods=['patch'], permission_classes=[IsBookingOwner])
    def update_number_of_people(self, request):
        booking_id = request.data.get('id')
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        serializer = BookingUpdateSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Booking updated successfully!', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def get_bookings(self, request):
      user_bookings = Booking.objects.filter(user=request.user)
      if not user_bookings.exists():
          return Response({"message": "No bookings found for the user."}, status=status.HTTP_404_NOT_FOUND)
      serializer = BookingSerializer(user_bookings, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False,methods=['get'],permission_classes=[IsBookingOwner])
    def retrieve_booking(self, request, slug=None):
          try:
              booking = get_object_or_404(Booking,slug=slug)
              serializer = BookingDetailSerializer(booking)
              return Response(serializer.data, status=status.HTTP_200_OK)
          except Packages.DoesNotExist:
              return Response({"error": "package not found"}, status=status.HTTP_404_NOT_FOUND)

  