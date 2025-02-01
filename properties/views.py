from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views.generic import View
from django.core.paginator import Paginator
from properties.models import Mess, MessMenu, Property, Review
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg

# Create your views here.

class PropertyListView(LoginRequiredMixin, View):
    
    template_name = 'property_list.html'
    items_per_page = 6
    
    def handle_no_permission(self):
        messages.error(self.request, 'Please sign in to view properties')
        return redirect('signin')

    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('search', '')
        
        # Get flats
        flats = Property.objects.filter(property_type='FLAT')
        
        # Get PG/Hostels
        pg_hostels = Property.objects.filter(property_type__in=['PG', 'HOSTEL'])
        
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
    

class PropertyDetailView(View):
    template_name = 'property_detail.html'
    reviews_per_page = 3
    
    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        property = Property.objects.get(id=id)
        
        # Get initial 3 reviews
        initial_reviews = property.reviews.all().order_by('-created_at')[:self.reviews_per_page]
        total_reviews = property.reviews.count()
        
        # Calculate average rating
        avg_rating = property.reviews.aggregate(Avg('rating'))['rating__avg']
        
        # Check if user has already reviewed
        user_review = None
        can_review = False
        if request.user.is_authenticated:
            user_review = property.reviews.filter(user=request.user).first()
            can_review = user_review is None
        
        context = {
            'property': property,
            'reviews': initial_reviews,
            'avg_rating': avg_rating,
            'user_review': user_review,
            'can_review': can_review,
            'total_reviews': total_reviews,
            'has_more_reviews': total_reviews > self.reviews_per_page
        }
        
        return render(request, self.template_name, context)


class AddPropertyReviewView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        property = Property.objects.get(id=id)
        
        # Check if user already reviewed
        if property.reviews.filter(user=request.user).exists():
            messages.error(request, 'You have already reviewed this property')
            return redirect('property-detail', pk=id)
            
        # Create review
        rating = request.POST.get('rating')
        description = request.POST.get('description')
        
        Review.objects.create(
            user=request.user,
            property=property,
            rating=rating,
            description=description,
            review_type='PROPERTY'
        )
        
        messages.success(request, 'Review added successfully')
        return redirect('property-detail', pk=id)


class PropertyReviewsAPIView(View):
    reviews_per_page = 3
    
    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        page = int(request.GET.get('page', 1))
        
        start = (page - 1) * self.reviews_per_page
        end = page * self.reviews_per_page
        
        property = Property.objects.get(id=id)
        reviews = property.reviews.all().order_by('-created_at')[start:end]
        
        reviews_data = [{
            'user': review.user.username,
            'rating': review.rating,
            'description': review.description,
            'created_at': review.created_at.strftime('%b %d, %Y')
        } for review in reviews]
        
        return JsonResponse({
            'reviews': reviews_data,
            'has_more': property.reviews.count() > end
        })

        
class MessListView(LoginRequiredMixin, View):
    template_name = 'mess_list.html'
    items_per_page = 6
    
    def handle_no_permission(self):
        messages.error(self.request, 'Please sign in to view messes')
        return redirect('signin')
    
    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('search', '')
        
        # Get all messes
        messes = Mess.objects.all()
        
        # Apply search if query exists
        if search_query:
            search_filter = Q(name__icontains=search_query) | \
                          Q(address__icontains=search_query) | \
                          Q(city__icontains=search_query)
                          
            messes = messes.filter(search_filter)
            
        messes = messes.order_by('-created_at')
        
        # Add pagination
        paginator = Paginator(messes, self.items_per_page)
        page = request.GET.get('page', 1)
        mess_list = paginator.get_page(page)
        
        context = {
            'messes': mess_list,
            'search_query': search_query
        }
        
        return render(request, self.template_name, context)
    
    
class MessMenuDetailView(View):
    template_name = 'mess_menu_detail.html'
    reviews_per_page = 3
    
    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        mess = Mess.objects.get(id=id)
        
        # Get menu items ordered by day
        day_order = dict((day, i) for i, (day, _) in enumerate(MessMenu.DAYS_OF_WEEK))
        menu_items = mess.menu.all()
        sorted_menu = sorted(menu_items, key=lambda x: day_order[x.day])
        
        # Get initial reviews
        initial_reviews = mess.reviews.all().order_by('-created_at')[:self.reviews_per_page]
        total_reviews = mess.reviews.count()
        
        # Calculate average rating
        avg_rating = mess.reviews.aggregate(Avg('rating'))['rating__avg']
        
        # Check if user has already reviewed
        user_review = None
        can_review = False
        if request.user.is_authenticated:
            user_review = mess.reviews.filter(user=request.user).first()
            can_review = user_review is None
        
        context = {
            'mess': mess,
            'menu_items': sorted_menu,
            'reviews': initial_reviews,
            'avg_rating': avg_rating,
            'user_review': user_review,
            'can_review': can_review,
            'total_reviews': total_reviews,
            'has_more_reviews': total_reviews > self.reviews_per_page
        }
        
        return render(request, self.template_name, context)
    

class AddMessReviewView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        mess = Mess.objects.get(id=id)
        
        # Check if user already reviewed
        if mess.reviews.filter(user=request.user).exists():
            messages.error(request, 'You have already reviewed this mess')
            return redirect('mess-menu-detail', pk=id)
            
        # Create review
        rating = request.POST.get('rating')
        description = request.POST.get('description')
        
        Review.objects.create(
            user=request.user,
            mess=mess,
            rating=rating,
            description=description,
            review_type='MESS'
        )
        
        messages.success(request, 'Review added successfully')
        return redirect('mess-menu-detail', pk=id)
    
    
class MessReviewsAPIView(View):
    reviews_per_page = 3
    
    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        page = int(request.GET.get('page', 1))
        
        start = (page - 1) * self.reviews_per_page
        end = page * self.reviews_per_page
        
        mess = Mess.objects.get(id=id)
        reviews = mess.reviews.all().order_by('-created_at')[start:end]
        
        reviews_data = [{
            'user': review.user.username,
            'rating': review.rating,
            'description': review.description,
            'created_at': review.created_at.strftime('%b %d, %Y')
        } for review in reviews]
        
        return JsonResponse({
            'reviews': reviews_data,
            'has_more': mess.reviews.count() > end
        })