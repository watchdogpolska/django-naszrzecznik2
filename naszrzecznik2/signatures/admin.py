from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from import_export.admin import ImportExportModelAdmin

from .models import Category, Petition, Signature
from .resources import SignatureResource


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    '''
        Admin View for Category
    '''
    list_display = ('name', )
    search_fields = ('name', )


@admin.register(Petition)
class PetitionAdmin(admin.ModelAdmin):
    '''
        Admin View for Petition
    '''
    list_display = ('title', 'active', 'category', 'created')
    list_filter = ('category', )
    search_fields = ('title', 'text')


@admin.register(Signature)
class SignatureAdmin(ImportExportModelAdmin):
    """
        Admin View for Signature
    """
    resource_class = SignatureResource
    list_display = ('petition', 'organization_name', 'first_name', 'second_name', 'place', 'email')
    search_fields = ('organization_name', 'first_name', 'second_name', 'place', 'email', )
    readonly_fields = ('location_picker', )

    def location_picker(self, obj):
        return '<input class="vTextField" id="locationinput" type="text"><br>' + \
            '<div id="map_canvas"></div>'
    location_picker.allow_tags = True
    location_picker.short_description = _("Location picker")

    class Media:
        js = [
            '//maps.googleapis.com/maps/api/js?sensor=false&libraries=places',
            '//ajax.googleapis.com/ajax/libs/jquery/1.7/jquery.min.js',
            '//cdn.rawgit.com/Logicify/jquery-locationpicker-plugin/9318afa450d13d26944d36dea99b60cfc6241dd0/src/locationpicker.jquery.js',
            '/static/petition/map_admin.js',
        ]
        css = {"all": ('/static/petition/map_admin.css', )}
