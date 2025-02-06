import random
from django.db import models

def uniqueID():
    custom_id = [str(random.randint(0, 9)) for _ in range(8)]
    return ''.join(custom_id)

class IntegerIDField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['unique'] = True
        kwargs['default'] = uniqueID
        kwargs['max_length'] = 100
        super().__init__(*args, **kwargs)


