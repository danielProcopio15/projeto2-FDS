from django.db import models
from django.contrib.auth.models import User


class ThemeAccess(models.Model):
	"""Track how many times a user visited a theme/category page.

	This is used to compute the "Para você" box on the home page.
	"""
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	category = models.CharField(max_length=100)
	count = models.PositiveIntegerField(default=0)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together = ("user", "category")
		indexes = [models.Index(fields=["user", "category"])]

	def __str__(self):
		return f"{self.user.username} — {self.category}: {self.count}"

	def increment(self, save=True):
		self.count = (self.count or 0) + 1
		if save:
			self.save()
		return self.count
