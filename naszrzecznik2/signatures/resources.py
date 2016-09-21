from import_export import resources
from .models import Signature


class SignatureResource(resources.ModelResource):
    class Meta:
        model = Signature
