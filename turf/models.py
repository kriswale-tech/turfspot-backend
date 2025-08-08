from django.db import models

class TurfSpot(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
    )

    name = models.CharField(max_length=100)
    turf_type = models.CharField(max_length=50, help_text="e.g. 7 a side")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    
    open_weekdays = models.CharField(max_length=100, help_text="e.g. Monday - Friday (6AM - 11PM)", blank=True, null=True)
    open_weekends = models.CharField(max_length=100, help_text="e.g. Saturday & Sunday (8AM - 11PM)", blank=True, null=True)

    distance = models.CharField(max_length=50, help_text="e.g. 1km from City Center", blank=True, null=True)
    location = models.CharField(max_length=200, help_text="e.g. Area, City, Country", blank=True, null=True)
    map_link = models.URLField(help_text="Google Maps link to the turf location", blank=True, null=True)

    # Store multiple phone numbers as comma-separated values
    contacts = models.TextField(help_text="Comma-separated phone numbers", blank=True, null=True)

    # WhatsApp and call fields (if you want specific buttons)
    whatsapp_number = models.CharField(max_length=20, help_text="WhatsApp number for direct messages", blank=True, null=True)
    call_number = models.CharField(max_length=20, help_text="Phone number for direct calls", blank=True, null=True)

    # Facilities as comma-separated string
    facilities = models.TextField(help_text="Comma-separated facilities like Floodlights, Parking Space, etc.", blank=True, null=True)

    # Upload multiple images
    main_image = models.ImageField(upload_to='turf_images/', blank=True, null=True)
    image1 = models.ImageField(upload_to='turf_images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='turf_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='turf_images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='turf_images/', blank=True, null=True)

    def __str__(self):
        return self.name
