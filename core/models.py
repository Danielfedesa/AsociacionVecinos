from django.db import models
from django.utils.text import slugify

class Activity(models.Model):
    SPORTS = "sports"
    CRAFTS = "crafts"
    CATEGORY_CHOICES = [(SPORTS, "Deportiva"), (CRAFTS, "Manualidades")]

    name = models.CharField("Nombre", max_length=120)
    slug = models.SlugField(unique=True, max_length=140, help_text="Se genera automáticamente si se deja vacío", blank=True)
    category = models.CharField("Categoría", max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField("Descripción", blank=True)
    image = models.ImageField(upload_to="activities/", blank=True, null=True) 

    class Meta:
        verbose_name = "Actividad"
        verbose_name_plural = "Actividades"
        ordering = ["category", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:140]
        super().save(*args, **kwargs)


class Session(models.Model):
    # un horario de una actividad concreta
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="sessions")
    day_of_week = models.IntegerField(choices=[
        (0,"Lunes"),(1,"Martes"),(2,"Miércoles"),(3,"Jueves"),(4,"Viernes"),(5,"Sábado"),(6,"Domingo")
    ])
    start_time = models.TimeField("Inicio")
    end_time = models.TimeField("Fin")
    is_active = models.BooleanField("Activa", default=True)

    class Meta:
        ordering = ["day_of_week", "start_time"]
        verbose_name = "Horario"
        verbose_name_plural = "Horarios"

    def __str__(self):
        return f"{self.activity.name} {self.get_day_of_week_display()} {self.start_time}-{self.end_time}"


class Announcement(models.Model):
    # Tablón de anuncios de la portada
    title = models.CharField("Título", max_length=140)
    body = models.TextField("Contenido")
    published_at = models.DateTimeField("Publicado", auto_now_add=True)
    is_pinned = models.BooleanField("Destacado", default=False)

    class Meta:
        ordering = ["-is_pinned", "-published_at"]
        verbose_name = "Anuncio"
        verbose_name_plural = "Anuncios"

    def __str__(self):
        return self.title