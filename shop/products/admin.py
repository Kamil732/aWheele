from django.contrib import admin

from .models import Car, ImageCar, Part, ImagePart, Motorcycle, ImageMotorcycle

class CarImageAdmin(admin.TabularInline):
    model = ImageCar
    extra = 0

class CarAdmin(admin.ModelAdmin):
    model = Car
    readonly_fields = ('id', 'slug',)
    inlines = [CarImageAdmin]

class PartImageAdmin(admin.TabularInline):
    model = ImagePart
    extra = 0

class PartAdmin(admin.ModelAdmin):
    model = Part
    readonly_fields = ('id', 'slug',)
    inlines = [PartImageAdmin]

class MotorcycleImageAdmin(admin.TabularInline):
    model = ImageMotorcycle
    extra = 0

class MotorcycleAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'slug',)
    model = Motorcycle
    inlines = [MotorcycleImageAdmin]

admin.site.register(Car, CarAdmin)
admin.site.register(Part, PartAdmin)
admin.site.register(Motorcycle, MotorcycleAdmin)