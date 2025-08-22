from celery import shared_task
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Recipe, Rating
from .models import Recipe
import datetime
from django.db import models
import csv
import boto3
from io import StringIO


@shared_task
def resize_recipe_image(recipe_id):
    """Asynchronously resize recipe images to max 800x800."""
    try:
        recipe = Recipe.objects.get(id=recipe_id)
        if recipe.image:
            img = Image.open(recipe.image.path)
            img.thumbnail((800, 800))

            buffer = BytesIO()
            img.save(buffer, format="JPEG", quality=85)

            recipe.image.save(
                recipe.image.name,
                ContentFile(buffer.getvalue()),
                save=True
            )
            print(f"✅ Resized image for recipe {recipe_id}")
    except Recipe.DoesNotExist:
        print(f"❌ Recipe {recipe_id} not found")
    except Exception as e:
        print(f"⚠️ Error resizing image for recipe {recipe_id}: {e}")


User = get_user_model()


@shared_task
def send_daily_email():
    """Send daily digest emails at 6AM, skipping weekends."""
    today = datetime.date.today()

    # Skip Saturday (5) & Sunday (6)
    if today.weekday() in [5, 6]:
        print("⏩ Weekend, skipping emails")
        return

    users = User.objects.all()
    for user in users:
        try:
            send_mail(
                subject="Daily Recipe Digest",
                message="Good morning! Check out new recipes today 🍳",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False, 
            )
            print(f"📧 Email sent to {user.email}")
        except Exception as e:
            print(f"⚠️ Failed to send email to {user.email}: {e}")

    print("✅ Daily emails sent")


@shared_task
def weekly_user_export_to_s3():
    csv_buffer = StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerow([
        "user_id", "username", "email", "is_seller",
        "recipe_id", "recipe_name", "recipe_description",
        "rating_count", "avg_rating",
        "created_at"
    ])

    users = User.objects.all()

    for user in users:
        recipes = Recipe.objects.filter(author=user).all()
        if recipes.exists():
            for recipe in recipes:
                avg_rating = Rating.objects.filter(recipe=recipe).aggregate(avg=models.Avg("score"))["avg"] or 0
                rating_count = Rating.objects.filter(recipe=recipe).count()

                writer.writerow([
                    user.id, user.username, user.email, user.is_staff, 
                    recipe.id, recipe.name, recipe.description,
                    rating_count, avg_rating,
                    recipe.created_at
                ])
        else:
            # User with no recipes
            writer.writerow([
                user.id, user.username, user.email, user.is_staff,
                None, None, None, 0, 0, None
            ])

    # Upload to S3
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )

    file_name = f"user_exports/all_users_{datetime.date.today()}.csv"

    s3_client.put_object(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=file_name,
        Body=csv_buffer.getvalue(),
        ContentType="text/csv"
    )

    print(f"✅ Exported all user data to S3: {file_name}")