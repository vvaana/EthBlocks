from django.db import models

# Create your models here.
class BlockInfo(models.Model):
    height = models.IntegerField(blank=True, null=True)
    hash = models.CharField(max_length=264, unique=True)
    n_tx = models.IntegerField(blank=True, null=True)
    depth = models.IntegerField(blank=True, null=True)
    received_time = models.DateTimeField(blank=True, null=True)
    prev_block = models.CharField(max_length=264)
    next_block = models.CharField(max_length=264, blank=True, null=True)
    prev_block_url = models.CharField(max_length=1000)
    next_block_url = models.CharField(max_length=1000, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.hash

