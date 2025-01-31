from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator
from properties.models import Property
from django.db.models import Q

# Create your views here.

class PropertyListView(View):
    
    template_name = 'property_list.html'
    items_per_page = 6

    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('search', '')
        
        # Get flats
        flats = Property.objects.filter(property_type='FLAT', available=True)
        
        # Get PG/Hostels
        pg_hostels = Property.objects.filter(property_type__in=['PG', 'HOSTEL'], available=True)
        
        # Apply search if query exists
        if search_query:
            search_filter = Q(title__icontains=search_query) | \
                          Q(address__icontains=search_query) | \
                          Q(city__icontains=search_query)
            
            flats = flats.filter(search_filter)
            pg_hostels = pg_hostels.filter(search_filter)

        # Order by created date
        flats = flats.order_by('-created_at')
        pg_hostels = pg_hostels.order_by('-created_at')

        # Paginate flats
        flat_paginator = Paginator(flats, self.items_per_page)
        flat_page = request.GET.get('flat_page', 1)
        flat_properties = flat_paginator.get_page(flat_page)

        # Paginate PG/Hostels
        pg_paginator = Paginator(pg_hostels, self.items_per_page)
        pg_page = request.GET.get('pg_page', 1)
        pg_properties = pg_paginator.get_page(pg_page)

        context = {
            'flat_properties': flat_properties,
            'pg_properties': pg_properties,
            'search_query': search_query,
        }
        
        return render(request, self.template_name, context)