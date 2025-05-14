from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from .forms import ReviewForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

@login_required
def review_list(request):
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(reviews, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_reviews': reviews.count(),
    }
    return render(request, 'reviews/list.html', context)

@login_required
def create_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, user=request.user)
        if form.is_valid():
            review = form.save()
            messages.success(request, 'Review submitted successfully!')
            return redirect('reviews:list')
    else:
        form = ReviewForm(user=request.user)
    
    context = {
        'form': form,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    }
    return render(request, 'reviews/create.html', context)

@login_required
def edit_review(request, pk):
    review = get_object_or_404(Review, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated successfully!')
            return redirect('reviews:list')
    else:
        form = ReviewForm(instance=review, user=request.user)
    
    context = {
        'form': form,
        'review': review,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    }
    return render(request, 'reviews/edit.html', context)

@login_required
@require_POST
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk, user=request.user)
    review.delete()
    messages.success(request, 'Review deleted successfully!')
    return redirect('reviews:list')

def review_stats(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    reviews = Review.objects.filter(user=request.user)
    stats = {
        'total': reviews.count(),
        'positive': reviews.filter(sentiment='positive').count(),
        'negative': reviews.filter(sentiment='negative').count(),
        'neutral': reviews.filter(sentiment='neutral').count(),
        'average_rating': reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0,
    }
    
    return JsonResponse(stats)
