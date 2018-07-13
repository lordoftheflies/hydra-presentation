import json

from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models

#
# class StaticComponentModel(models.Model):
#     source = models.CharField(max_length=1000, null=True, blank=True, default=None)
#
#
# # Create your models here.
# class HyperlinkModel(models.Model):
#     name = models.CharField(max_length=1000, null=True, blank=True, default=None)
#     label = models.CharField(max_length=1000, null=True, blank=True, default=None)
#     url = models.URLField(max_length=1000)
#
#     class Meta:
#         managed = False
#
#
# class ApplicationModel(models.Model):
#     name = models.CharField(max_length=1000, null=True, blank=True, default=None)
#     title = models.CharField(max_length=1000, null=True, blank=True, default=None)
#     url = models.URLField(max_length=1000)
#     main_menus = models.ManyToManyField(to=HyperlinkModel, related_name='applications')
#
#     class Meta:
#         managed = False
#
#
# class PageModel(StaticComponentModel):
#     name = models.CharField(max_length=1000, null=True, blank=True, default=None)
#     title = models.CharField(max_length=1000, null=True, blank=True, default=None)
#     url = models.URLField(max_length=1000)
#     application = models.ForeignKey(to=ApplicationModel, on_delete=models.CASCADE, related_name='pages')
#
#     class Meta:
#         managed = False
#
#
# class DynamicComponentModel(StaticComponentModel):
#     name = models.CharField(max_length=1000, null=True, blank=True, default=None)
#     styles = JSONField(max_length=1000, null=True, blank=True, default=None)
#     components = JSONField(max_length=1000, null=True, blank=True, default=None)
#
#     style = JSONField(max_length=1000, null=True, blank=True, default=None)
#     content = models.TextField(max_length=1000, null=True, blank=True, default=None)
#
#     code = models.TextField(max_length=1000, null=True, blank=True, default=None)
#
#     class Meta:
#         managed = False
#
#
# class PropertyModel(models.Model):
#     name = models.CharField(max_length=1000, null=True, blank=True, default=None)
#     type = models.CharField(max_length=1000, null=True, blank=True, default=None)
#     notify = models.NullBooleanField(max_length=1000, null=True, blank=True, default=None)
#     reflect_to_attribute = models.NullBooleanField(max_length=1000, null=True, blank=True, default=None)
#     value = models.CharField(max_length=1000, null=True, blank=True, default=None)
#     component = models.ForeignKey(to=DynamicComponentModel, on_delete=models.CASCADE, related_name='properties')
#
#     class Meta:
#         managed = False
#
#     def __str__(self):
#         representation = dict(
#             name=self.name,
#             type=self.type,
#             notify=self.notify,
#             reflectToAttribute=self.reflect_to_attribute,
#             value=self.value
#         )
#         return json.dumps(representation)
#
#
# class ObserverModel(models.Model):
#     name = models.CharField(max_length=1000, null=True, blank=True, default=None)
#     parameters = ArrayField(null=True, blank=True, default=None)
#     component = models.ForeignKey(to=DynamicComponentModel, on_delete=models.CASCADE, related_name='observers')
#
#     class Meta:
#         managed = False
#
#     def __str__(self):
#         return '%s(%s)' % (
#             self.name,
#             (', '.join(self.parameters))
#         )
#
#
# class FormModel(models.Model):
#     name = models.CharField(max_length=1000, null=True, blank=True, default=None)
#     title = models.CharField(max_length=1000, null=True, blank=True, default=None)
#
#     class Meta:
#         managed = False
#
#
# class TagModel(models.Model):
#     name = models.CharField(max_length=1000, null=True, blank=True, default=None)
#     content = models.CharField(max_length=1000, null=True, blank=True, default=None)
#
#     class Meta:
#         managed = False
#
#
# class TagAttribute(models.Model):
#     name = models.CharField(max_length=1000, null=True, blank=True, default=None)
#     value = models.CharField(max_length=1000, null=True, blank=True, default=None)
#     owner = models.ForeignKey(to=TagModel, on_delete=models.CASCADE)
#
#     class Meta:
#         managed = False
#
#
# class FieldModel(models.Model):
#     name = models.CharField(max_length=1000, null=True, blank=True, default=None)
#     label = models.CharField(max_length=1000, null=True, blank=True, default=None)
#     type = models.CharField(max_length=1000, null=True, blank=True, default=None)
#     editor = models.ForeignKey(to=TagModel, on_delete=models.CASCADE, related_name='editors')
#     display = models.ForeignKey(to=TagModel, on_delete=models.CASCADE, related_name='displays')
#
#     class Meta:
#         managed = False
# # class TagAttribute(models.Model):
# #     name = models.CharField(max_length=1000, null=True, blank=True, default=None)
# #     value = models.CharField(max_length=1000, null=True, blank=True, default=None)
# #     editor = models.ForeignKey(to=TagModel, on_delete=models.CASCADE)
