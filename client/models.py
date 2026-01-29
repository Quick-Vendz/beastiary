from django.db import models
from django.utils.text import slugify

class Book(models.Model):
    index = models.IntegerField()
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)

    class Meta:
        ordering = ['index']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chapters')
    index = models.IntegerField()
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, null=True)

    class Meta:
        unique_together = ['book', 'slug']
        ordering = ['book', 'index']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def first_page(self):
        """Get the first page in this chapter"""
        return self.pages.filter(parent=None).first()

    def __str__(self):
        return self.title


class Page(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='pages')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='pages', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subpages', blank=True, null=True)
    index = models.IntegerField()
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, null=True)
    content = models.TextField(blank=True)

    class Meta:
        unique_together = [['book', 'chapter', 'slug']]
        ordering = ['book__index', 'chapter__index', 'index']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
