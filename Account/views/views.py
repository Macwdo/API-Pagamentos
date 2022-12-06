from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def get_bd(request):
    if request.method == 'GET':
        data = {
                'NAME': os.getenv('DATABASE_NAME'),
                'HOST': os.getenv('DATABASE_HOST'),
                'PASSWORD': os.getenv('DATABASE_PASSWORD'),
                'USER': os.getenv('DATABASE_USER'),
                'PORT': os.getenv('DATABASE_PORT')
            }
        return Response(data=data)