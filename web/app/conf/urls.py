from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title='Funbox schema v1',
        default_version='v1',
        description='TEST swagger for funbox',
    ),
    public=True,
)


urlpatterns = [
    path('', include('core.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
]
