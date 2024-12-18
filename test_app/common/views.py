from datetime import timezone, timedelta

from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render, get_object_or_404

from test_app.blog.models import Plant, Category, Post, Comment


# Create your views here

def HomeView(request):
    categories = Category.objects.all()
    featured_posts = [
        {
            "title": "Indoor Plants Care",
            "description": "Learn how to take care of your indoor plants and create a green oasis at home.",
            "image": "images/indoor_plants.jpg",
            "category_name": "Indoor",
        },
        {
            "title": "Succulent Care",
            "description": "Discover the best tips for growing and maintaining beautiful succulents.",
            "image": "images/suculents.jpg",
            "category_name": "Succulents",
        },
        {
            "title": "Outdoor Gardening",
            "description": "Get tips for creating the perfect garden and growing plants outdoors.",
            "image": "images/outdoor_plants.jpg",
            "category_name": "Outdoor",
        },
    ]

    context = {
        "featured_posts": featured_posts,
        "categories": categories,
    }
    return render(request, "home/home.html", context)


def plants_by_category(request, category_name):
    category = get_object_or_404(Category, name=category_name)

    plants = Plant.objects.filter(category=category)

    context = {
        "plants": plants,
        "category_name": category.name,
    }

    return render(request, 'blog/plant_list.html', context)




