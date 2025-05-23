from rest_framework import serializers
from .models import Book, Author, Category

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id','name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=True, read_only=True)
    category = CategorySerializer(many=True, read_only=True)
    stars = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'description',
            'release',
            'cover',
            'author',
            'category',
            'price',
            'oneStarCount',
            'twoStarCount',
            'threeStarCount',
            'fourStarCount',
            'fiveStarCount',
            'stars'
            ]
        
    def get_stars(self, obj):
            return obj.stars
    
class BookWriteSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Author.objects.all()
    )
    category = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all()
    )

    class Meta:
        model = Book
        fields = [
            'title', 'description', 'release', 'cover',
            'author', 'category', 'price',
            'oneStarCount', 'twoStarCount', 'threeStarCount',
            'fourStarCount', 'fiveStarCount',
        ]
