from django.core.management.base import BaseCommand
from inventory_app.models import Category, Product
from django.contrib.auth.models import User
from django.core.files import File
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        # Create categories
        categories = ['Electronics', 'Books', 'Home & Kitchen', 'Toys']
        for cat in categories:
            Category.objects.get_or_create(name=cat)

        # Create products
        products = [
            ('Smartphone X', 'Latest smartphone with advanced features', 899.99, 'Electronics', 50, 'smartphone.jpg'),
            ('Laptop Pro', 'High-performance laptop for professionals', 1299.99, 'Electronics', 30, 'laptop.jpg'),
            ('Python Mastery', 'Comprehensive guide to Python programming', 39.99, 'Books', 100, 'python_book.jpg'),
            ('Coffee Maker Deluxe', 'Automatic coffee maker with multiple settings', 79.99, 'Home & Kitchen', 40, 'coffee_maker.jpg'),
            ('Robot Building Kit', 'Educational toy for young engineers', 59.99, 'Toys', 60, 'robot_kit.jpg'),
        ]

        for name, desc, price, cat, stock, image_name in products:
            category = Category.objects.get(name=cat)
            product, created = Product.objects.get_or_create(
                name=name,
                defaults={
                    'description': desc,
                    'price': price,
                    'category': category,
                    'stock': stock
                }
            )
            if created:
                image_path = os.path.join(settings.BASE_DIR, 'sample_images', image_name)
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as image_file:
                        product.image.save(image_name, File(image_file), save=True)
                else:
                    self.stdout.write(self.style.WARNING(f'Image not found: {image_path}'))

        # Create a test user
        User.objects.create_user(username='testuser', password='testpassword')

        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))