from django.db import models


class Search(models.Model):
    Search_value = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.Search_value)


    class Meta:
        verbose_name_plural = "Searches"


class Product(models.Model):
    Name = models.CharField(max_length=100, null=True, blank=True)
    Price = models.CharField(max_length=10, null=True, blank=True)
    Link = models.CharField(max_length=300, null=True, blank=True)
    Image = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.Name)


    class Meta:
        verbose_name_plural = "Products"