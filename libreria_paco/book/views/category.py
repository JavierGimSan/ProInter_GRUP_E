from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Category
from ..serializers import CategorySerializer

@api_view(["GET"])
def get_all_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
def create_category(request):
    serializer = CategorySerializer(data=request.data)
    if not serializer.is_valid(): return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["PATCH"])
def patch_category(request, id: int):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    new_name = request.data.get("name", None)
    if not new_name: return Response({"error": "Name not set"})
    category.name = new_name
    category.save()
    serializer = CategorySerializer(category)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["DELETE"])
def delete_category(request, id: int):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    category.delete()
    return Response({"message": "Category deleted successfully"})