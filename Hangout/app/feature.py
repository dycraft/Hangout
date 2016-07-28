from .models import Activity, User
import math

'''
symmetrical==False means that change obj1 but not change obj2
'''
def update_feature(obj1, obj2, symmetrical=True):
	pass


def feature_length(feature):
	result = 0
	for i in range(0, len(feature)):
		result += int(feature[i]) ** 2
	result = math.sqrt(result)
	if result == 0:
		return 1
	else:
		return result

def feature_inner_product(f1, f2):
	length = len(f1)
	result = 0
	for i in range(0, length):
		result += int(f1[i]) * int(f2[i])
	return result

def similarity(f1, f2):
	if not len(f1) == len(f2):
		return -1
	else:
		return feature_inner_product(f1, f2) / (feature_length(f1) * feature_length(f2)) 

def compare_construct(user):
	def cmp(a, b):
		x = similarity(a.feature, user.feature) 
		y = similarity(b.feature, user.feature)
		if x < y:
			return -1
		elif x > y:
			return 1
		else:
			return 0
	return cmp