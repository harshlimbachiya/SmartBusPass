from django.db import models

# Existing Category model, simplified as you requested
class Category(models.Model):
    categoryname = models.CharField(max_length=100, null=True)
    creationDate = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.categoryname


# Location model for Source and Destination (Predefined locations)
class Location(models.Model):
    name = models.CharField(max_length=300, unique=True)  # Name of the location (e.g., city, station)

    def __str__(self):
        return self.name


# RouteCost model to store cost based on Source-Destination
class RouteCost(models.Model):
    source = models.ForeignKey(Location, related_name='source_location', on_delete=models.CASCADE)
    destination = models.ForeignKey(Location, related_name='destination_location', on_delete=models.CASCADE)
    base_cost = models.DecimalField(max_digits=10, decimal_places=2)  # Base cost for the route

    def __str__(self):
        return f"Cost from {self.source.name} to {self.destination.name}"


class Pass(models.Model):
    PassNumber = models.CharField(max_length=200)
    FullName = models.CharField(max_length=200, null=True)
    ContactNumber = models.CharField(max_length=15, null=True)
    Email = models.CharField(max_length=100, null=True)
    IdentityType = models.CharField(max_length=200, null=True)
    IdentityCardno = models.CharField(max_length=200, null=True)
    
    # ForeignKey to Category (Daily, Monthly, Quarterly)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    # ForeignKey to Location for Source and Destination
    Source = models.ForeignKey(Location, related_name='source_location_pass', on_delete=models.CASCADE)
    Destination = models.ForeignKey(Location, related_name='destination_location_pass', on_delete=models.CASCADE)

    FromDate = models.DateField(null=True)
    ToDate = models.DateField(null=True)
    
    # Cost will be set based on the selected category and route
    Cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    PasscreationDate = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def set_cost(self):
        """
        Method to set cost based on the Source and Destination using the RouteCost model.
        This fetches the base cost from the RouteCost model.
        The final cost is then calculated based on the category type (Daily, Monthly, Quarterly).
        """
        try:
            # Fetch the route cost from RouteCost model based on source and destination
            route_cost = RouteCost.objects.get(source=self.Source, destination=self.Destination)
            base_cost = route_cost.base_cost

            # Calculate the cost based on the pass category
            if self.category.categoryname == 'Daily':
                self.Cost = base_cost * 1  # For daily pass, use the base cost directly.
            elif self.category.categoryname == 'Monthly':
                self.Cost = base_cost * 30  # For monthly pass, multiply by 30 (assuming daily rate).
            elif self.category.categoryname == 'Quarterly':
                self.Cost = base_cost * 90  # For quarterly pass, multiply by 90 (assuming daily rate).
            else:
                self.Cost = base_cost  # Default to base cost if no valid category found.

        except RouteCost.DoesNotExist:
            self.Cost = 0  # If no route cost is found, set cost to 0.
    def generate_pass_number(self):
        """
        Generates a unique pass number if it's not already set.
        """
        if not self.PassNumber:
            self.PassNumber = str(uuid.uuid4().hex[:10]).upper() 

    def save(self, *args, **kwargs):
        self.set_cost()  # Always calculate cost before saving

        super(Pass, self).save(*args, **kwargs)

    def __str__(self):
        return self.PassNumber


# Contact model for queries or messages from users
class Contact(models.Model):
    name = models.CharField(max_length=200, null=True)
    emailid = models.CharField(max_length=100, null=True)
    contact = models.CharField(max_length=15, null=True)
    message = models.CharField(max_length=300, null=True)
    msgdate = models.DateField(null=True)
    isread = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.emailid


# Payment model to track payments for each pass
class Payment(models.Model):
    pass_instance = models.ForeignKey(Pass, on_delete=models.CASCADE)  # Link to the Pass model
    payment_date = models.DateTimeField(auto_now_add=True)  # Date of payment
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount paid
    payment_status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending')
    
    # You could also add a payment method here like card, cash, etc.
    payment_method = models.CharField(max_length=100, null=True, blank=True)  
    
    def __str__(self):
        return f"Payment for {self.pass_instance.PassNumber} - {self.payment_status}"
