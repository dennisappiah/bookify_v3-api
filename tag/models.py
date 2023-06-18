from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

"""creating custom manager for querying taggedItems"""


class TaggedItemManager(models.Manager):
    def get_tags_for(self, object_type, object_id):
        content_type = ContentType.objects.get_for_model(object_type)

        return TaggedItem.objects.select_related('tag').filter(content_type=content_type, object_id=object_id)


"""Creating Generic Relationships"""


class Tag(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label


class TaggedItem(models.Model):
    """
    - what tag applied to what object (Book, Article..)

    -We need two things to identify the object:
    content Type (book, article) and ID of particular object
    """
    objects = TaggedItemManager()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
