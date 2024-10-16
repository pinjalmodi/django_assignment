from django.db import models

# Create your models here.
class User(models.Model):
	usertype=models.CharField(max_length=100,choices = (
		('admin','admin' ),
		('product_manager','product_manager')
		))
	fname=models.CharField(max_length=100)
	mobile=models.PositiveIntegerField()
	email=models.EmailField()
	address=models.TextField()
	password=models.CharField(max_length=100)
	profile_picture=models.ImageField(upload_to='profile_picture/',default="")
	def __str__(self):
		return self.fname+"-"+self.usertype


class Product_mst(models.Model):
	product_id=models.PositiveIntegerField(primary_key=True)
	product_name=models.CharField(max_length=100)
	def __str__(self):
		return self.product_name

class Product_sub_cat(models.Model):
	product_id=models.PositiveIntegerField()
	product_price=models.PositiveIntegerField()
	product_image=models.ImageField(upload_to='product_image/',default="")
	product_model=models.CharField(max_length=100)
	product_ram=models.PositiveIntegerField()
	product_name=models.ForeignKey(Product_mst,on_delete=models.CASCADE)

	def __str__(self):
		return "{} - {}".format(self.product_name.product_name, self.product_model)