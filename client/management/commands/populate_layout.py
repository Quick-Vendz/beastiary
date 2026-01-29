from django.core.management.base import BaseCommand
from client.models import Book, Chapter, Page


class Command(BaseCommand):
    help = 'Populate database from layout.txt'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before populating',
        )

    def handle(self, *args, **options):
        # Only clear if explicitly requested
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            Page.objects.all().delete()
            Chapter.objects.all().delete()
            Book.objects.all().delete()
        else:
            self.stdout.write(self.style.NOTICE('Keeping existing data. Use --clear to delete first.'))

        # Read layout file
        with open('layout.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()

        current_book = None
        current_chapter = None
        indent_stack = {}  # Maps indent level to the last page at that level

        book_index = 1
        chapter_index = 1
        page_index = 1

        for line in lines:
            if not line.strip():
                continue
            
            # Count indentation (4 spaces per level)
            indent_level = (len(line) - len(line.lstrip())) // 4
            content = line.strip()
            
            if content.startswith('Book:'):
                title = content.replace('Book:', '').strip()
                current_book, created = Book.objects.get_or_create(
                    index=book_index,
                    defaults={'title': title}
                )
                if created:
                    self.stdout.write(f"Created Book: {title}")
                else:
                    self.stdout.write(f"Found existing Book: {title}")
                book_index += 1
                current_chapter = None
                indent_stack = {}
                page_index = 1
                chapter_index = 1
            
            elif content.startswith('Chapter:'):
                title = content.replace('Chapter:', '').strip()
                current_chapter, created = Chapter.objects.get_or_create(
                    book=current_book,
                    index=chapter_index,
                    defaults={'title': title}
                )
                if created:
                    self.stdout.write(f"  Created Chapter: {title}")
                else:
                    self.stdout.write(f"  Found existing Chapter: {title}")
                chapter_index += 1
                indent_stack = {}
                page_index = 1
            
            elif content.startswith('Page:'):
                title = content.replace('Page:', '').strip()
                
                # Determine parent: look for last page at indent_level - 1
                parent = None
                if indent_level > 1:  # Level 0 is Book, 1 is Chapter or top-level page
                    parent_level = indent_level - 1
                    parent = indent_stack.get(parent_level)
                
                # Generate slug - for child pages, prefix with parent slug
                from django.utils.text import slugify
                if parent:
                    slug = f"{parent.slug}-{slugify(title)}"
                else:
                    slug = slugify(title)
                
                page, created = Page.objects.get_or_create(
                    book=current_book,
                    chapter=current_chapter,
                    slug=slug,
                    defaults={
                        'parent': parent,
                        'index': page_index,
                        'title': title,
                    }
                )
                
                if not created:
                    # Update existing page if needed
                    page.parent = parent
                    page.index = page_index
                    page.title = title
                    page.save()
                
                # Store this page at its indent level (and clear deeper levels)
                indent_stack[indent_level] = page
                # Clear all deeper levels
                keys_to_remove = [k for k in indent_stack.keys() if k > indent_level]
                for k in keys_to_remove:
                    del indent_stack[k]
                
                page_index += 1
                
                indent_str = "  " * (indent_level + 1)
                parent_str = f" (parent: {parent.title})" if parent else ""
                action = "Created" if created else "Updated"
                self.stdout.write(f"{indent_str}{action} Page: {title}{parent_str}")

        self.stdout.write(self.style.SUCCESS(f"\n✓ Database populated successfully!"))
        self.stdout.write(f"Total Books: {Book.objects.count()}")
        self.stdout.write(f"Total Chapters: {Chapter.objects.count()}")
        self.stdout.write(f"Total Pages: {Page.objects.count()}")
