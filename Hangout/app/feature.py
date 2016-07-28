from .models import Activity, User
import Math

def update_feature(act, user):
	pass


def feature_length(feature):
	result = 0
	for i in range(0, len(feature)):
		result += int(feature[i]) ** 2
	result = Math.sqrt(result)
	return result

def feature_inner_product(f1, f2):
	length = len(f1)
	result = 0
	for x in range(0, length):
		result += int(f1[i]) * int(f2[i])
	return result

def similarity(f1, f2):
	if not len(f1) == len(f2):
		return -1
	else:
		return feature_inner_product(f1, f2) / (feature_length(f1) * feature_length(f2)) 