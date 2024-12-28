from ..serializers.bankist_serializer import (
    BankistSerializer,
    Bankist, 
    TransferSerializer,
    TransactionHistorySerialier,
    TransactionHistory,
    DepositSeriaizer
    )
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import SessionAuthentication
from rest_framework import status


class WithdrawApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    def post(self, request):
        
        #validate user authentication
        if not request.user.is_authenticated:
            return Response({"error": "You must be logged in to perform this action."}, status=status.HTTP_401_UNAUTHORIZED)

        #check if the user has bank account
        try:
            sender_bank_account = Bankist.objects.get(user_profile__user=request.user)
        except Bankist.DoesNotExist:
            return Response({"error": "Account doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TransferSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            reciver_account_number = serializer.validated_data['reciver_account_number']
            pin = serializer.validated_data['pin']
            
            
            if reciver_account_number == sender_bank_account.account_number:
                return Response({"message":"you can't send to your self"},status=status.HTTP_403_FORBIDDEN)
            
            #check the reciver account
            try:
                reciver_bank_account = Bankist.objects.get(account_number= reciver_account_number)
            except Bankist.DoesNotExist:
                return Response({"error":"reciver account doesn't exist"},status=status.HTTP_404_NOT_FOUND)
            
            # Validate PIN
            if not sender_bank_account.check_pin(pin):
                return Response(
                    {"message": "PIN doesn't match. Please try again!"},
                    status=status.HTTP_403_FORBIDDEN
                )

            # Check for sufficient balance
            if sender_bank_account.balance < amount:
                return Response(
                    {"message": "Insufficient balance!","balance":f"your balance is {sender_bank_account.balance}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Perform withdrawal
            sender_bank_account.balance -= amount
            reciver_bank_account.balance += amount
            sender_transaction = TransactionHistory.objects.create(
                bank_account = sender_bank_account,
                amount = -amount,
                transaction_type = TransactionHistory.Status.TRANSFER
                
            )
            
            receiver_transaction = TransactionHistory.objects.create(
                bank_account = reciver_bank_account,
                amount = amount,
                transaction_type = TransactionHistory.Status.TRANSFER
                
            )
            
            sender_transaction.related_transaction = receiver_transaction
            sender_transaction.save()
            sender_bank_account.save()
            reciver_bank_account.save()
            return Response({
                "message": "Transaction successful",
                "balance": f"Your new balance is {sender_bank_account.balance}",
                "receiver": f"Money successfully sent to {reciver_bank_account.user_profile.user.username}"}, 
                status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        # Handle PIN updates
        try:
            bank_account = Bankist.objects.get(user_profile__user=request.user)
        except Bankist.DoesNotExist:
            return Response({"error": "Account doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        # Validate input data
        serializer = TransferSerializer(data=request.data)
        if serializer.is_valid():
            new_pin = serializer.validated_data['pin']

            # Update the PIN
            bank_account.set_pin(new_pin)
            bank_account.save()
            return Response({"message": "PIN updated successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  
class CreateBankAccount(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        serializer = BankistSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class DepositApiView(APIView):
    def patch(self,request):
        try:
            depositer_bank_account = Bankist.objects.get(user_profile__user = request.user)
        except Bankist.DoesNotExist:
            return Response({"error":"account doesn't exist. create bank account or login with valid credntials"},status=status.HTTP_403_FORBIDDEN)
        serializer = DepositSeriaizer(data = request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            pin = serializer.validated_data['pin']
            
            if not depositer_bank_account.check_pin(pin):
                return Response({"error":"incorrect pin please try again"},status=status.HTTP_403_FORBIDDEN)
            depositer_bank_account.balance += amount
            depositer_transaction_history = TransactionHistory.objects.create(
                bank_account = depositer_bank_account,
                amount = amount,
                transaction_type = TransactionHistory.Status.DEPOSIT
                
            )
            depositer_bank_account.save()
            depositer_transaction_history.save()
            return Response({
                "message": "successfully Deposit to your account",
                "balance": f"Your new balance is {depositer_bank_account.balance}"}, 
                status=status.HTTP_200_OK
                )
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class BankAccountsApiView(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
      bank_accounts = Bankist.objects.all().select_related('user_profile')
      serializer = BankistSerializer(bank_accounts,many=True)
      
      return Response(serializer.data)