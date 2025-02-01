from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from customer.models import User
from django.core.exceptions import ValidationError

# Create your models here.


class PropertyOwner(models.Model):
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "amenities"

    def __str__(self):
        return self.name

class Property(models.Model):
    PROPERTY_TYPES = [
        ('PG', 'Paying Guest'),
        ('FLAT', 'Flat'),
        ('HOSTEL', 'Hostel'),
    ]

    GENDER_CHOICES = [
        ('M', 'Gents'),
        ('F', 'Ladies'),
        ('MX', 'Mixed'),
    ]

    FURNISHING_CHOICES = [
        ('FF', 'Fully Furnished'),
        ('SF', 'Semi Furnished'),
        ('NF', 'Non Furnished'),
    ]

    BATHROOM_TYPE_CHOICES = [
        ('COMMON', 'Common'),
        ('SINGLE', 'Single'),
        ('ATTACHED', 'Attached'),
    ]

    # Basic Property Information
    title = models.CharField(max_length=200)
    property_type = models.CharField(max_length=10, choices=PROPERTY_TYPES)
    description = models.TextField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    available = models.BooleanField(default=True)
    
    # Owner Information
    owner = models.ForeignKey(PropertyOwner, on_delete=models.CASCADE)
    
    # Financial Details
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    maintenance_charge = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Property Specifications
    gender_type = models.CharField(max_length=2, choices=GENDER_CHOICES)
    
    # Amenities
    amenities = models.ManyToManyField(Amenity)
    
    # Flat-specific fields
    furnishing_type = models.CharField(
        max_length=2, 
        choices=FURNISHING_CHOICES, 
        blank=True, 
        null=True
    )
    bedroom_count = models.PositiveIntegerField(blank=True, null=True)
    bathroom_count = models.PositiveIntegerField(blank=True, null=True)
    
    # PG and Hostel specific fields
    bathroom_type = models.CharField(
        max_length=10, 
        choices=BATHROOM_TYPE_CHOICES, 
        blank=True, 
        null=True
    )
    persons_per_room = models.PositiveIntegerField(blank=True, null=True)
    mess_included = models.BooleanField(default=False)
    
    # location
    latitude = models.CharField(max_length=100, null=True, blank=True)
    longitude = models.CharField(max_length=100, null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Validate flat-specific fields
        if self.property_type == 'FLAT':
            if not self.furnishing_type:
                raise ValidationError('Furnishing type is required for flats')
            if not self.bedroom_count:
                raise ValidationError('Bedroom count is required for flats')
            if not self.bathroom_count:
                raise ValidationError('Bathroom count is required for flats')
        
        # Validate PG and Hostel specific fields
        if self.property_type in ['PG', 'HOSTEL']:
            if not self.bathroom_type:
                raise ValidationError('Bathroom type is required for PG/Hostel')
            if not self.persons_per_room:
                raise ValidationError('Number of persons per room is required for PG/Hostel')

    def __str__(self):
        return f"{self.title} - {self.get_property_type_display()}"

    class Meta:
        verbose_name_plural = "properties"

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')
    

# Proxy models for PG/hostels and flat

class PGHostelProperty(Property):
    class Meta:
        proxy = True
        verbose_name = 'PG/Hostel Property'
        verbose_name_plural = 'PG/Hostel Properties'

class FlatProperty(Property):
    class Meta:
        proxy = True
        verbose_name = 'Flat Property'
        verbose_name_plural = 'Flat Properties'
        

class Mess(models.Model):
    MEAL_TYPES = [
        ('VEG', 'Vegetarian'),
        ('NON_VEG', 'Non-Vegetarian'),
        ('BOTH', 'Both')
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    monthly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    contact_number = models.CharField(max_length=15, null=True)
    meal_type = models.CharField(max_length=10, choices=MEAL_TYPES)
    is_snacks_available = models.BooleanField(default=False)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    available = models.BooleanField(default=True)
    latitude = models.CharField(max_length=100, null=True, blank=True)
    longitude = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Messes"
        
    def __str__(self):
        return self.name
    

class MessMenu(models.Model):
    DAYS_OF_WEEK = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday')
    ]
    
    mess = models.ForeignKey(Mess, on_delete=models.CASCADE, related_name='menu')
    day = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    breakfast = models.CharField(max_length=300)
    lunch = models.CharField(max_length=300)
    dinner = models.CharField(max_length=300)
    
    def __str__(self):
        return self.day
    
    
    
class Review(models.Model):
    # Review types
    REVIEW_TYPES = [
        ('PROPERTY', 'Property Review'),
        ('MESS', 'Mess Review')
    ]
    
    # Foreign keys
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    property = models.ForeignKey('Property', on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    mess = models.ForeignKey('Mess', on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    
    # Review content
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField()
    review_type = models.CharField(max_length=10, choices=REVIEW_TYPES)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        # Ensure one review per user per property/mess
        unique_together = [
            ('user', 'property'),
            ('user', 'mess')
        ]

    def clean(self):
        
        # Validate either property or mess is set, but not both
        if self.property and self.mess:
            raise ValidationError("A review can't be for both property and mess")
        if not self.property and not self.mess:
            raise ValidationError("A review must be for either a property or mess")
        
        # Set review type based on what's being reviewed
        if self.property:
            self.review_type = 'PROPERTY'
        elif self.mess:
            self.review_type = 'MESS'

    def __str__(self):
        if self.property:
            return f"Review for {self.property.title} by {self.user.username}"
        return f"Review for {self.mess.name} by {self.user.username}"