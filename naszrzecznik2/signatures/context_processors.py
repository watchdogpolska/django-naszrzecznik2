from .models import Category


def get_petition_category_list(self):
    return {'petition_category_list': Category.objects.all()}
