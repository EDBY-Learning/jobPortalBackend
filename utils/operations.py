from rest_framework.response import Response
import random 

def update_with_partial(self, request,  *args, **kwargs):
    partial = kwargs.pop('partial', True)
    instance = self.get_object()
    self.check_object_permissions(request,instance)
    serializer = self.get_serializer(instance, data=request.data, partial=partial)
    serializer.is_valid(raise_exception=True)
    self.perform_update(serializer)
    return Response(serializer.data)

def generate_random_hash():
    return abs(hash(str(random.randint(1000000,5000000)))) % (10 ** 8)