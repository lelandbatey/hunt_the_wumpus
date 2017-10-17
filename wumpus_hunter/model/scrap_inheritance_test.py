import json
#pylint: disable=W0312
#pylint: disable=C0330

class Aobj(object):
	"""docstring for Aobj"""
	def __init__(self, first, second, third):
		self.first = first
		self.second = second
		self.third = third
	def __str__(self): 
		return json.dumps({
				'first' : self.first,
				'second' : self.second,
				'third' : self.third 
			},
			sort_keys=True, indent=4, separators=(',', ': '))

class Bobj(Aobj):
	"""docstring for Bobj"""
	def __init__(self, first, second, third):
		super().__init__(first, second, third)

class Cobj(Aobj):
	"""docstring for Cobj"""
	def __init__(self, first, second, third):
		super().__init__()
		self.first = first
		self.second = second
		self.third = third
		

a = Aobj(1, 2, 3)
b = Bobj(10, 20, 30)
c = Cobj(11, 22, 33)

print(a)
print(b)
print(c)


