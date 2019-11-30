import random
from statistics import median
import copy

class Schedule():
	#courses is a dictionary as class -> list_of_list[subject,frequency,instructor].
	#days->time_slots->courses
	#list->list->list
	#assuming all classes have move more than 5 events per week.


	"""
	days = [Mon, Tues, Wedenes, ....]
	time_slots  = [9:15-10:45,.... in order]
	classes = {
					class1 : [[Subject1, frequency, instructor], [Subject2, frequenecy, instructor],....]
						.
						.
						.
		}
	"""
	
	def make_timetable(self, time_slots, days, classes):
		#timetable is a dictionary.
		timetable = {}
		#past_events = []
		#at all days, first slot is always occupied.
		time_slots = self.time_slots[:]
		courses =  [[k,v] for k, v in self.classes.items()]
		#courses = [[classes,[sub,freq,instructor]]] 
		random.shuffle(self.days)
		for i in self.days:
			timetable[i] = {}
			for j in courses:
				while(True):
					m = random.randrange(0,len(j[1]),1)
					if j[1][m][1]!= 0 :
						try:
							timetable[i][time_slots[0]].append([j[0],j[1][m][0],j[1][m][2]])
						except:
							timetable[i][time_slots[0]] = []
							timetable[i][time_slots[0]].append([j[0],j[1][m][0],j[1][m][2]])
						j[1][m][1] -= 1
						break
		"""
	program according to that all the courses are allotted.
	make a list of list == [[class,sub,instructor],...all events] s.t. if freq = 2, then that element occurs twice in list.
		"""
		
		events = []
		for k in self.classes:
			for j in self.classes[k]:
				while(j[1]!=0):
					events.append([k,j[0],j[2]])
					j[1] -= 1
		
		random.shuffle(events)
		time_slots.pop(0)
		random.shuffle(self.days)
		for i in events:
			while(True):
				for k in days:
					r = random.randrange(0,len(time_slots),1)
					try:
						timetable[k][time_slots[r]].append(i)
					except:
						timetable[k][time_slots[r]] = []
						timetable[k][time_slots[r]].append(i)
					random.shuffle(self.days)
					break
				break
		return timetable


	
	def evaluate_coinciding_lectures(self):
		for i in self.timetable:
			# i === day	
				# j == time_slot
				for k in self.timetable[i]:
					container = []
					# k === [[class, subject, instructor]]
					for j in self.timetable[i][k]:
						if j[0] not in container:
							container.append(j[0])
						else:
							return False
					print (container)
		return True

	
	def evaluate_coinciding_instructors(self):
		for i in self.timetable:
			# i === day	
				# j == time_slot
				for k in self.timetable[i]:
					container = []
					# k === [[class, subject, instructor]]
					for j in self.timetable[i][k]:
						if j[2] not in container:
							container.append(j[2])
						else:
							return False
					print (container)
		return True

	
	def same_subject_not_more_than_once(self):
		for i in self.timetable:
			container = []
			slots_courses = [[s,v] for s,v in self.timetable[i].items()]
			for k in slots_courses:
				l = 0
				while(l<len(k[1])): 
					entry = [k[1][l][0],k[1][l][1]]
					if entry not in container:
						container.append(entry)
					else:
						return False
					l += 1
		return True
#WE CANNOT CALL SELF.TIMETABLE method IN EVALUATION METHODS SINCE IT WILL CREATE A RANDOM TIMETABLE AND THEN CHECK FOR IT.

	
	def instructor_rest(self):
		for i in self.timetable:
			container = []
			# j == time->courses dictionary
			for j in i:
				slots_courses = [[s,v] for s,v in j.items()]
				for k in slots_courses:
					entry = [k[0],k[1][2]]
					container.append(entry)
				i = 0
				while(i<len(self.time_slots)):
					j = 0
					while j<len(container)-2:
						if(container[j][1] == container[j+1][1]):
							if(container[j+1][1] == container[j+2][1]):
								return False
						j += 1
					i += 1
		return True

	

	def fitness(self):
		fitness = 0
		if(self.evaluate_coinciding_lectures()):
			fitness += 0.4
		if(self.evaluate_coinciding_instructors()):
		 	fitness += 0.4
		if(self.same_subject_not_more_than_once()):
		 	fitness += 0.2

		return fitness

	

	def __init__(self, time_slots, days, classes):
		print("started")
		self.time_slots = time_slots
		self.days = days 
		self.classes = classes
		print (classes)
		print (time_slots)
		print (days)
		self.timetable = self.make_timetable(time_slots, days, classes)
		self.fitness = self.fitness()

"""				
			Schedule === {
							MONDAY : {
											9:00 - 10:45   :   [[Class1,Subject,Instructor],[Class2,Subject,Instructor],....]
											.
											.
											.
									}
								.
								.
								.
						}

"""

class Population:
	def population(self, chromosomes):
		return [Schedule() for x in range(chromosomes)]

	def __init__(self, chromosomes = 50):
		self.chromosomes = chromosomes
		self.population = population(chromosomes)

	def selection(self):
		fitness_ = []
		for i in self.population:
			fitness_.append(i.fitness)
		median = statistics.median(fitness)
		selected = []
		for i in self.population:
			if(i.fitness > median):
				selected.append(i)
		return selected

	def pairing(self, selected):
		if(len(selected)%2!=0):
			fitness_ = []
			for i in selected:
				fitness_.append(i.fitness)
			sick = min(fitness_)
			for i in selected:
				if(i.fitness == sick):
					selected.remove(i)
		random.shuffle(selected)
		paired = []
		for i in range(len(selected)):
			paired.append([selected[i],selected[i+1]])
		return paired
