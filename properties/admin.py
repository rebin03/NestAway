from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html

from customer.models import User
from properties.models import Property, PropertyOwner, PropertyImage, Amenity, PGHostelProperty, FlatProperty, Mess, MessMenu, Review

# Register your models here.

# Image Preview Inline
class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1  # Number of empty forms to display
    
    # Optional: Add image preview
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'
    
    readonly_fields = ['image_preview']
    fields = ['image', 'image_preview']


@admin.register(PropertyOwner)
class PropertyOwnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email')
    search_fields = ('name', 'phone_number', 'email')


@admin.register(PGHostelProperty)
class PGHostelPropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'property_type', 'city', 'monthly_rent', 'gender_type', 'available')
    list_filter = ('property_type', 'city', 'gender_type', 'available', 'mess_included')
    search_fields = ('title', 'description', 'address', 'city', 'owner__name')
    filter_horizontal = ('amenities',)
    inlines = [PropertyImageInline]  # Add the image inline

    # Fields to display in the form
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'property_type', 'description', 'owner')
        }),
        ('Location', {
            'fields': ('address', 'city', 'latitude', 'longitude')
        }),
        ('Financial Details', {
            'fields': ('monthly_rent', 'security_deposit', 'maintenance_charge')
        }),
        ('Property Specifications', {
            'fields': ('gender_type', 'mess_included', 'bathroom_type', 
                      'persons_per_room')
        }),
        ('Amenities', {
            'fields': ('amenities',)
        }),
        ('Status', {
            'fields': ('available',)
        })
    )

    def get_queryset(self, request):
        # Only show PG and Hostel properties
        return super().get_queryset(request).filter(property_type__in=['PG', 'HOSTEL'])

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "property_type":
            kwargs['choices'] = [('PG', 'Paying Guest'), ('HOSTEL', 'Hostel')]
        return super().formfield_for_choice_field(db_field, request, **kwargs)

   
@admin.register(FlatProperty)
class FlatPropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'monthly_rent', 'bedroom_count', 'furnishing_type', 'available')
    list_filter = ('city', 'furnishing_type', 'bedroom_count', 'available')
    search_fields = ('title', 'description', 'address', 'city', 'owner__name')
    filter_horizontal = ('amenities',)
    inlines = [PropertyImageInline]  # Add the image inline

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'property_type', 'description', 'owner')
        }),
        ('Location', {
            'fields': ('address', 'city', 'latitude', 'longitude')
        }),
        ('Financial Details', {
            'fields': ('monthly_rent', 'security_deposit')
        }),
        ('Flat Specifications', {
            'fields': ('furnishing_type', 'bedroom_count', 'bathroom_count')
        }),
        ('Additional Details', {
            'fields': ('gender_type',)
        }),
        ('Amenities', {
            'fields': ('amenities',)
        }),
        ('Status', {
            'fields': ('available',)
        })
    )

    def get_queryset(self, request):
        # Only show Flat properties
        return super().get_queryset(request).filter(property_type='FLAT')

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "property_type":
            kwargs['choices'] = [('FLAT', 'Flat')]
        return super().formfield_for_choice_field(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.property_type = 'FLAT'  # Ensure property type is always 'FLAT'
        super().save_model(request, obj, form, change)


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    
    
class MessMenuInline(admin.TabularInline):
    model = MessMenu
    extra = 7  # Show all 7 days
    max_num = 7
    
    # def get_initial(self):
    #     # Pre-populate days of the week
    #     return [{'day': day[0]} for day in MessMenu.DAYS_OF_WEEK]

@admin.register(Mess)
class MessAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'monthly_rate', 'meal_type', 'available')
    list_filter = ('city', 'meal_type', 'available')
    search_fields = ('name', 'description', 'address', 'city')
    inlines = [MessMenuInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'meal_type', 'contact_number', 'is_snacks_available')
        }),
        ('Location', {
            'fields': ('address', 'city', 'latitude', 'longitude')
        }),
        ('Financial Details', {
            'fields': ('monthly_rate', 'daily_rate')
        }),
        ('Timing Details', {
            'fields': ('opening_time', 'closing_time')
        }),
        ('Status', {
            'fields': ('available',)
        })
    )
    
    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    # Display fields in list view
    list_display = ('user', 'review_type', 'rating', 'created_at')
    
    # Filter options
    list_filter = ('review_type', 'rating', 'created_at')
    
    # Search fields
    search_fields = ('user__username', 'property__title', 'mess__name', 'description')
    
    # Make all fields readonly
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return ('user', 'property', 'mess', 'rating', 'description', 'review_type', 'created_at', 'updated_at')
        return ('created_at', 'updated_at')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

    # Organize fields in fieldsets
    fieldsets = (
        ('Review Details', {
            'fields': ('user', 'property', 'mess', 'rating', 'description')
        }),
        ('Metadata', {
            'fields': ('review_type', 'created_at', 'updated_at')
        })
    )



# Custom admin site to modify the admin index
class SearchifyAdminSite(admin.AdminSite):
    site_header = 'Searchify Admin'
    site_title = 'Searchify Admin Portal'
    index_title = 'Property Management'

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request)
        # Customize the admin index to show clear separation between property types
        return app_list

admin_site = SearchifyAdminSite(name='searchify_admin')

# Register models with the custom admin site
admin_site.register(User)
admin_site.register(PropertyOwner, PropertyOwnerAdmin)
admin_site.register(PGHostelProperty, PGHostelPropertyAdmin)
admin_site.register(FlatProperty, FlatPropertyAdmin)
admin_site.register(Amenity, AmenityAdmin)
admin_site.register(Mess, MessAdmin)
admin_site.register(Review, ReviewAdmin)