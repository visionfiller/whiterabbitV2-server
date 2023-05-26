from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from whiterabbitapi.views import VarietalView, RegionView, VarietalRegionView, CustomerView, EmployeeView, register_user, login_user, UserView, WineTypeView, AcidityView, BodyView, DrynessView, WineBottleView
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'varietals', VarietalView, 'varietal')
router.register(r'varietalregions', VarietalRegionView, 'varietalregion')
router.register(r'regions', RegionView, 'region')
router.register(r'acidities', AcidityView, 'acidity')
router.register(r'bodies', BodyView, 'body')
router.register(r'drynesses', DrynessView, 'dryness')
router.register(r'winetypes', WineTypeView, 'winetype')
router.register(r'winebottles', WineBottleView, 'winebottle')
router.register(r'customers', CustomerView, 'customer')
router.register(r'employees', EmployeeView, 'employee')
router.register(r'users', UserView, 'user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register', register_user),
    path('login', login_user),
    path('', include(router.urls))
]
