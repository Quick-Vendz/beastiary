from django.shortcuts import render, get_object_or_404
from .models import Book, Chapter, Page


def home(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'client/home.html', context)


def page_view(request, book_slug, page_slug, chapter_slug=None):
    book = get_object_or_404(Book, slug=book_slug)
    
    if chapter_slug:
        chapter = get_object_or_404(Chapter, book=book, slug=chapter_slug)
        page = get_object_or_404(Page, book=book, chapter=chapter, slug=page_slug)
    else:
        # Page directly under book (no chapter)
        page = get_object_or_404(Page, book=book, chapter=None, slug=page_slug)
        chapter = None
    
    # Get navigation items
    chapters = book.chapters.all()
    pages = book.pages.filter(chapter=None, parent=None)  # Top-level pages
    
    context = {
        'book': book,
        'chapter': chapter,
        'page': page,
        'chapters': chapters,
        'pages': pages,
    }
    return render(request, 'client/page.html', context)
