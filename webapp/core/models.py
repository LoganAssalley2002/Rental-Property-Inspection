import string
from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return self.user.username

    @property
    def initial(self):
        initial = 'a'

        if self.user.first_name:
            initial = self.user.first_name[0].lower()
        elif self.user.last_name:
            initial = self.user.last_name[0].lower()
        elif self.user.username:
            initial = self.user.username[0].lower()
        else:
            initial = 'a'

        if initial in string.ascii_lowercase:
            return initial
        else:
            return 'a'

    @property
    def picture(self):
        return static(f'core/assets/profile_svg/{self.initial}.svg')


class Property(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    name = models.CharField(max_length=128)
    address = models.TextField()

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'


class Inspection(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    inspector = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inspections_conducted')
    inspected_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inspections_received')
    inspected_property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='inspections', blank=True, null=True)

    @property
    def is_completed(self):
        if self.inspected_property and self.areas.exists():
            return True
        return False


class Area(models.Model):
    inspection = models.ForeignKey(Inspection, related_name='areas', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} in {self.inspection.inspected_property.address}"


def area_image_folder(instance, filename):
    '''File will be uploaded to MEDIA_ROOT/inspection_<id>/area_<id>/<filename>'''
    return f'inspection_{instance.area.inspection.id}/area_{instance.area.id}/{filename}'


class AreaImage(models.Model):
    area = models.ForeignKey(Area, related_name='images', on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=area_image_folder)

    def __str__(self):
        return f"Image for {self.area.name} in {self.area.inspection.inspected_property.address}"


    class Meta:
        verbose_name = 'Area Image'
        verbose_name_plural = 'Area Images'













































