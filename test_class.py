import sys
import socket
import random

class person(object):

	def __init__(self, name, age): #instantitate person object
		self.name = name
		self.age = age
		self.id = ''
		self.salary = ''
		self.position = ''
		self.status = ''
		
	def getName(self): #return name of person
		return self.name

	def getAge(self): #return age of person
		return self.age

	def getId(self): #return age of person
		return self.id

	def changeName(self, new_name): #change persons name
		self.name = new_name
		print('Name has been changed to %s' % new_name)

	def changeAge(self, new_age): #change persons age
		self.age = new_age
		print('Name has been changed to %s' % new_age)

	def generateId(self): #generate ID for person object
		self.id = random.randint(1,1000)

	def createPosition(self, position): #assign position to person
		self.position = position

	def updateStatus(self, status): #change persons status (Active or inactive)
		self.status = status

	def updateSalary(self, salary): #update persons salary
		self.salary = salary

def main():
	ans = 'y'
	while (ans == 'y'):
		name = input("Please enter employee name: ")
		age = input("Please enter employees age: ")
		employee = person(name, age)
		name = employee.getName()
		print(name)
		age = employee.getAge()
		print(age)
		print('Generating employee ID')
		employee.generateId()
		id = employee.getId()
		print("ID is %s" % id)
		new_name = input("Please enter the new name for this employee: ")
		print('New name is %s' % new_name)
		new_age = input('Please enter the new age for this employee: ')
		employee.changeName(new_name)
		employee.changeAge(new_age)
		ans = input("Do you want to add another employee(y/n)")
		if ans == 'n': print('Quitting program...')


if __name__ == '__main__':
	main()
