from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views.user_views import (
  UserApiView,
  UserProfileApiView,
  TourGuiderApiView,
  UserCreationApiView
  )
from .views.packages_views import PackagesApiViews,SubPackageApiView,PackageReviewApiView,GetPakcages
from .views.bankist_view import WithdrawApiView,CreateBankAccount,DepositApiView,BankAccountsApiView
from .views.booking_views import BookingApiView,BookingPaymentApiView,BookingPackageApiView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

router = DefaultRouter()
router.register(r'user',UserCreationApiView,basename='user')
router.register(r'packages',PackagesApiViews)
router.register(r'subpackages',SubPackageApiView)
router.register(r'userprofile',UserProfileApiView)
router.register(r'bookings',BookingApiView)
router.register(r'tourguider',TourGuiderApiView)
router.register(r'packages_review',PackageReviewApiView)


urlpatterns = [
  path('api/',include(router.urls)),
  path('api/bankaccount/withdraw/',WithdrawApiView.as_view(),name='withdraw'),
  path('api/bankaccount/create_bank_account/',CreateBankAccount.as_view(),name='create_bank_account'),
  path('api/bankaccount/deposit/',DepositApiView.as_view(),name='deposit'),
  path('api/bankaccounts/',BankAccountsApiView.as_view(),name='bank_accounts'),
  path('api/booking_payment/',BookingPaymentApiView.as_view(),name='bank_accounts'),
  path('api/booking_package/',BookingPackageApiView.as_view(),name='booking_package'),
  path('api/get_packages/',GetPakcages.as_view(),name='get_packages'),
  path('bookings/<slug:slug>/', BookingApiView.as_view({'get': 'retrieve'}), name='booking-detial'),
  path('user/<slug:slug>/', UserCreationApiView.as_view({'get': 'retrieve_user'}), name='user-detail'),
]

# 50001343844932



# jwt path to sesssion authentication
urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
