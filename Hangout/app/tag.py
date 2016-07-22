from .models import Tag

def get_tag(name):
	
	try:
		tag = Tag.objects.get(name=name)
	except Tag.DoesNotExist:
		tag = Tag.objects.create(name=name)

	return tag