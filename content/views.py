from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Content, Rating
from .forms import ContentUploadForm,CollaborateUploadForm
from django.db.models import Q
from django.contrib import messages
from blog.models import Blog
# from django.core.mail import send_mail
from utils.email_utils import send_email
from .models import PromotedContent
from django.utils import timezone
from django.core.paginator import Paginator
from payments.models import PayPalTransaction


from payments.utils import process_payment 

def custom_404_view(request, exception=None):
    return render(request, "content/404_page.html", status=404)

def browse_content(request):
    query = request.GET.get("q", "")
    content_type = request.GET.get("content_type", "")
    sort_by = request.GET.get("sort_by", "latest")

    contents = Content.objects.all()

    if query:
        contents = contents.filter(Q(title__icontains=query) | Q(description__icontains=query))

    if content_type:
        contents = contents.filter(content_type=content_type)

    if sort_by == "popular":
        contents = contents.order_by("-views")
    elif sort_by == "latest":
        contents = contents.order_by("-uploaded_at")

    return render(request, "content/browse.html", {"contents": contents})


def home(request):
    contents = Content.objects.all()[:8]
    blogs = Blog.objects.filter(status='published').order_by('-created_at')[:4]
    promoted = PromotedContent.objects.filter(is_active=True, promotion_end__gte=timezone.now())
    all_content = Content.objects.all().exclude(id__in=[p.content.id for p in promoted])

    # return render(request, "home.html", {"promoted": promoted, "all_content": all_content})
    return render(request, 'content/home.html', {'contents': contents, 'blogs': blogs, "promoted": promoted, "promoted_all_content": all_content})

def category(request, content_type):
    type = content_type
    contents = Content.objects.filter(content_type=content_type).order_by('-uploaded_at')
    CONTENT_TYPES = [
        ('short_film', 'Short Film'),
        ('podcast', 'Podcast'),
        ('documentary', 'Documentary'),
        ('entertainment', 'Entertainment Project'),
        ('animation', 'Animation'),
        ('interviews', 'Interviews'),
        ('education', 'Education'),
        ('music', 'Music'),
        ('web_series', 'Web Series'),
    ]

    for i in range(0, len(CONTENT_TYPES)):
        if (CONTENT_TYPES[i][0]== content_type):
            content_type = CONTENT_TYPES[i][1]
            num = i+1
    


    return render(request, 'content/category.html', {'contents': contents, 'content_type': content_type, "num": str(num), 'type': type})

def genre(request, genre_type):
    contents = Content.objects.filter(genre=genre_type).order_by('-uploaded_at')
    GENRE_TYPE = [
        ('Comedy', 'Comedy'),
        ('Action', 'Action'),
        ('Romantic', 'Romantic'),
        ('Thriller', 'Thriller'),
        ('Horror', 'Horror'),
    ]

    for i in range(0, len(GENRE_TYPE)):
        if (GENRE_TYPE[i][0]== genre_type):
            genre_type = GENRE_TYPE[i][1]
            num = i+1
    
    
    return render(request, 'content/category.html', {'contents': contents, 'genre_type': genre_type, "num": str(num)})

def language(request, language_type):
    contents = Content.objects.filter(language=language_type).order_by('-uploaded_at')

    LANGUAGE_TYPE = [
        ('English', 'English'),
        ('Hindi', 'Hindi'),
        ('French', 'French'),
        ('Russian', 'Russian'),
        ('German', 'German'),
        ('Spanish', 'Spanish'),
    ]

    for i in range(0, len(LANGUAGE_TYPE)):
        if (LANGUAGE_TYPE[i][0] == language_type):
            language_type = LANGUAGE_TYPE[i][1]
            num = i+1

    return render(request, 'content/category.html', {'contents': contents, 'language_type': language_type, "num": str(num)})

@login_required
def upload_content(request):
    if request.method == 'POST':
        form = ContentUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            content = form.save(commit=False)
            content.uploaded_by = request.user.profile
            content.save()

            # Check if the user selected promotion
            if form.cleaned_data['promote']:
                duration = form.cleaned_data['promotion_duration']
                amount = 5 if duration == '7' else 15
                print(amount)
                request.session['promotion_content_id'] = content.id
                request.session['promotion_duration'] = duration
                # request.session['promotion_amount'] = amount
                return redirect('promote_content', content_id=content.id)  # Redirect to payment page

            return redirect('home')

    else:
        form = ContentUploadForm()

    return render(request, 'content/upload_content.html', {'form': form})

@login_required
def edit_content(request, pk):
    content = get_object_or_404(Content, pk=pk)

    # Ensure only the owner can edit
    if str(content.uploaded_by) != str(request.user):

        messages.error(request, "You do not have permission to edit this content.")
        return redirect('dashboard')

    if request.method == "POST":
        content.title = request.POST.get("title")
        content.description = request.POST.get("description")
        content.genre = request.POST.get("genre")
        content.age_rating = request.POST.get("age_rating")
        content.duration = request.POST.get("duration")
        content.cast = request.POST.get("cast")
        content.country = request.POST.get("country")
        content.language = request.POST.get("language")
        content.save()
        messages.success(request, "Content updated successfully!")
        return redirect('dashboard')

    return render(request, "content/edit_content.html", {"content": content})


@login_required
def rate_content(request, content_id):
    if request.method == "POST":
        content = get_object_or_404(Content, id=content_id)
        rating_value = int(request.POST.get("rating"))

        if rating_value < 1 or rating_value > 5:
            return JsonResponse({"error": "Invalid rating"}, status=400)

        rating, created = Rating.objects.update_or_create(
            user=request.user, content=content, defaults={"rating": rating_value}
        )

        # Update average rating
        all_ratings = content.ratings.all()
        total = sum(r.rating for r in all_ratings)
        content.total_ratings = all_ratings.count()
        content.average_rating = total / content.total_ratings if content.total_ratings > 0 else 0
        content.save()

        return JsonResponse({"message": "Rating submitted", "average_rating": content.average_rating})

@login_required
def promote_content(request, content_id):
    content = Content.objects.get(id=content_id)
    print(content)
    promotion_duration = request.session.get('promotion_duration', None)
    print(promotion_duration)

    if request.method == "POST":
        # duration = int(request.POST.get("promotion_amount"))  # Days
        
        duration = int(promotion_duration)  # Days
        amount = duration * 5  # Example: $5 per day
        # amount = promotion_amount

        # Process payment
        payment_status = process_payment(request.user, amount)
        if payment_status:
            promotion_end = timezone.now() + timezone.timedelta(days=int(duration))
            print(amount)
            PromotedContent.objects.create(
                creator=request.user,
                content=content,
                promotion_end=promotion_end,
                amount_paid=amount,
            )
            return redirect("home")  # Redirect to home after success

    return render(request, "content/promote_content.html", {"promotion_duration": int(promotion_duration)*5})

# @login_required
# def upload_content(request):

#     if request.method == 'POST':

#         form = ContentUploadForm(request.POST, request.FILES)
            
#         if form.is_valid():
#             content = form.save(commit=False)
#             content.uploaded_by = request.user.profile
#             content.save()
#             return redirect('home')
#     else:
#         form = ContentUploadForm()
#     return render(request, 'content/upload_content.html', {'form': form})

def content_detail(request, pk):
    content = get_object_or_404(Content, pk=pk)
    content.views += 1
    content.earnings += 1
    content.save()
    return render(request, 'content/content_detail.html', {'content': content})

def content_display(request, pk):
    content = get_object_or_404(Content, pk=pk)
    payments = PayPalTransaction.objects.filter(user=request.user, is_status_active=True)

    if payments:
        for payment in payments:
            if payment.payment_for == 'pay-per-view':
                if payment.used == True:
                    PayPalTransaction.objects.filter(user=request.user, paypal_order_id=payment.paypal_order_id, is_status_active=True).update(is_status_active=False)
                PayPalTransaction.objects.filter(user=request.user, paypal_order_id=payment.paypal_order_id, used=False).update(used=True)
            else:
                if payment.active_duration <= timezone.now():
                    PayPalTransaction.objects.filter(user=request.user, paypal_order_id=payment.paypal_order_id, is_status_active=True).update(is_status_active=False)
                    PayPalTransaction.objects.filter(user=request.user, paypal_order_id=payment.paypal_order_id, used=False).update(used=True)

                print(payment.active_duration , timezone.now(), payment.active_duration <= timezone.now())
    print(payments)
    return render(request, 'content/content_display.html', {'content': content, 'payment': payments})

@login_required
def collaborate(request):
    if request.method == 'POST':
        form = CollaborateUploadForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.save(commit=False)
            content.user = request.user
            content.save()

            # Prepare email content
            subject = "New Collaboration Submission"
            recipient_email = "accm8783@gmail.com"  # Change to the actual recipient's email
            sender_email = request.user.email  # Sender is the logged-in user's email
            message = f"""
            A new collaboration request has been submitted.

            User: {request.user.get_full_name()} ({request.user.email})
            
            Submission Details:
            ----------------------------
            """
            for field, value in form.cleaned_data.items():
                message += f"{field}: {value}\n"

            # Send the email
            send_email(subject, message, [recipient_email])


            return redirect('home')
    else:
        form = CollaborateUploadForm()
    return render(request, 'content/collaborate.html', {'form': form})




@login_required
def delete_content(request, pk):
    content = get_object_or_404(Content, pk=pk)

    print(content)
    # Ensure only the owner can delete their content
    if str(content.uploaded_by) != str(request.user):
        messages.error(request, "You do not have permission to delete this content.")
        return redirect('dashboard')  # Redirect to dashboard
    
    print(content)
    # if request.method == "POST":
    if request.method == "GET":
        print(content)
        content.delete()
        messages.success(request, "Content deleted successfully!")
        return redirect('dashboard')  # Redirect after deletion
    print(content)
    return render(request, "content/delete_confirm.html", {"content": content})



def free_content_list(request, content_type, show):
    if show == 'all':
        free_contents = Content.objects.filter(content_type = content_type).order_by('-uploaded_at')  # or use your free criteria
        paginator = Paginator(free_contents, 12)  # 10 items per page

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        free_contents = Content.objects.filter(is_premium=show, content_type = content_type).order_by('-uploaded_at')  # or use your free criteria
        paginator = Paginator(free_contents, 12)  # 10 items per page

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
    return render(request, 'content/free_content_list.html', {'page_obj': page_obj})
