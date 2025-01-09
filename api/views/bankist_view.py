from ..serializers.bankist_serializer import (
    BankistSerializer,
    Bankist, 
    TransferSerializer,
    TransactionHistorySerialier,
    TransactionHistory,
    DepositSeriaizer
    )
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import SessionAuthentication
from rest_framework import status


class BankistViewSet(viewsets.ViewSet):
    
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def create_bank_account(self, request):
        serializer = BankistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['get'])
    def check_account(self, request):
        try:
            bank_account = Bankist.objects.get(user_profile__user=request.user)
        except Bankist.DoesNotExist:
            return Response({"error": "Account doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BankistSerializer(bank_account)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(detail=False, methods=['post'])
    def withdraw(self, request):
        try:
            sender_bank_account = Bankist.objects.get(user_profile__user=request.user)
        except Bankist.DoesNotExist:
            return Response({"error": "Account doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TransferSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            receiver_account_number = serializer.validated_data['reciver_account_number']
            pin = serializer.validated_data['pin']

            if receiver_account_number == sender_bank_account.account_number:
                return Response({"message": "You can't send to yourself"}, status=status.HTTP_403_FORBIDDEN)

            try:
                receiver_bank_account = Bankist.objects.get(account_number=receiver_account_number)
            except Bankist.DoesNotExist:
                return Response({"error": "Receiver account doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

            if not sender_bank_account.check_pin(pin):
                return Response({"message": "Incorrect PIN. Please try again!"}, status=status.HTTP_403_FORBIDDEN)

            if sender_bank_account.balance < amount:
                return Response({"message": "Insufficient balance!", "balance": sender_bank_account.balance},
                                status=status.HTTP_400_BAD_REQUEST)

            sender_bank_account.balance -= amount
            receiver_bank_account.balance += amount

            sender_transaction = TransactionHistory.objects.create(
                bank_account=sender_bank_account, amount=-amount, transaction_type=TransactionHistory.Status.TRANSFER)
            receiver_transaction = TransactionHistory.objects.create(
                bank_account=receiver_bank_account, amount=amount, transaction_type=TransactionHistory.Status.TRANSFER)

            sender_transaction.related_transaction = receiver_transaction
            sender_transaction.save()
            sender_bank_account.save()
            receiver_bank_account.save()

            return Response({"message": "Transaction successful", "balance": sender_bank_account.balance},
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['patch'])
    def change_pin(self, request):
        try:
            bank_account = Bankist.objects.get(user_profile__user=request.user)
        except Bankist.DoesNotExist:
            return Response({"error": "Account doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TransferSerializer(data=request.data)
        if serializer.is_valid():
            new_pin = serializer.validated_data['pin']
            bank_account.set_pin(new_pin)
            bank_account.save()
            return Response({"message": "PIN updated successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['patch'])
    def deposit(self, request):
        try:
            depositer_bank_account = Bankist.objects.get(user_profile__user=request.user)
        except Bankist.DoesNotExist:
            return Response({"error": "Account doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DepositSeriaizer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            pin = serializer.validated_data['pin']

            if not depositer_bank_account.check_pin(pin):
                return Response({"error": "Incorrect PIN"}, status=status.HTTP_403_FORBIDDEN)

            depositer_bank_account.balance += amount
            depositer_transaction = TransactionHistory.objects.create(
                bank_account=depositer_bank_account, amount=amount, transaction_type=TransactionHistory.Status.DEPOSIT)

            depositer_bank_account.save()
            depositer_transaction.save()

            return Response({"message": "Deposit successful", "balance": depositer_bank_account.balance},
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['get'])
    def transaction_history(self, request):
        try:
            bank_account = Bankist.objects.get(user_profile__user=request.user)
        except Bankist.DoesNotExist:
            return Response({"error": "Account doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        transactions = TransactionHistory.objects.filter(bank_account=bank_account)
        serializer = TransactionHistorySerialier(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def get_accounts(self, request):
        bank_accounts = Bankist.objects.all().select_related('user_profile')
        serializer = BankistSerializer(bank_accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)