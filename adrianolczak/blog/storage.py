from pathlib import Path

from django.core.files.storage import FileSystemStorage


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        """
        If a filename already exists on the target storage system, delete it
        for new content to be written to.
        """
        if self.exists(name):
            self.delete(name)
        return name


def post_image_path(instance, filename):
    """
    Path relative to MEDIA_ROOT pointing to the post image storage
    """
    ext = filename.split(".")[-1]
    filename = f"{instance.slug}.{ext}"
    filepath = Path("posts") / "thumbnail" / filename

    return filepath


def post_content_images_path(instance, filename):
    """
    Path relative to MEDIA_ROOT pointing to the images belonging to the post content
    """
    post_id = str(instance.post.id)
    post_slug = instance.post.slug
    posts_path = Path("posts")
    return posts_path / f"{post_id}_{post_slug}" / filename
