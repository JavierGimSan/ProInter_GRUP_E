from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release = models.DateField()
    cover = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, related_name="books")

    oneStarCount = models.PositiveBigIntegerField()
    twoStarCount = models.PositiveBigIntegerField()
    threeStarCount = models.PositiveBigIntegerField()
    fourStarCount = models.PositiveBigIntegerField()
    fiveStarCount = models.PositiveBigIntegerField()

    @property
    def stars(self):
        stars = [self.oneStarCount, self.twoStarCount, self.threeStarCount, self.fourStarCount, self.fiveStarCount]
        totalCount = sum(stars)
        if totalCount == 0: return 0

        sumOfStars = sum(count * (idx + 1) for idx, count in enumerate(stars))

        return sumOfStars / totalCount

    def __str__(self):
        return f"{self.title} - {self.author}"
