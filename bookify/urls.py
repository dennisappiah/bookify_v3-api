from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register('v1/categories', views.CategoryViewSet)
router.register('v1/books', views.BookViewSet, basename="books")
router.register('v1/customers', views.CustomerViewSet)
router.register('v1/rentals', views.RentalViewSet)

book_router = routers.NestedDefaultRouter(router, 'v1/books', lookup='book')
book_router.register('comments', views.CommentViewSet, basename='book-comments')
book_router.register('images', views.BookImageViewSet, basename='book-images')

urlpatterns = router.urls + book_router.urls