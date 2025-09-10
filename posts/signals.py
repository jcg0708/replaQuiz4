import random
import string
from django.utils.text import slugify

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        # For Post model, use first 50 characters of content for slug
        if hasattr(instance, 'title') and instance.title:
            slug = slugify(instance.title)
        elif hasattr(instance, 'content') and instance.content:
            # Use first 50 characters of content for slug
            content_preview = instance.content[:50]
            slug = slugify(content_preview)
        else:
            # Fallback to random slug
            slug = f"post-{random_string_generator(size=8)}"

    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug)
    if qs.exists():
        new_slug = f"{slug}-{random_string_generator(size=4)}"
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug