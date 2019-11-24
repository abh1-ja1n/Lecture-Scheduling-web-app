import random

def make_timetable(time_slots, days, classes):
		#timetable is a dictionary.
		timetable = {}
		#past_events = []
		#at all days, first slot is always occupied.
		courses = [ [k,v] for k, v in self.classes.items() ]
		random.shuffle(self.days)
		for i in days:
			timetable[i] = {}
			for j in courses:
				while(True):
					r = random.randrange(0,len(courses),1)
					if courses[r][1][1]!= 0 :
						timetable[i][time_slots[0]] = [courses[r][0],courses[r][1][0],courses[r][1][2]]
						courses[r][1][1] -= 1
						break
		time_slots.pop(0)
		random.shuffle(self.days)
		random.shuffle(time_slots)
		random.shuffle(courses)
		for i in days:
			for j in courses:
				while(True):
					r = random.randrange(0,len(time_slots),1)
					if(j[1][1] != 0):
						timetable[i][time_slots[r]] = [j[0],j[1][0],j[1][2]]
						break
		#this timetable can have all 2 lectures of the same at a time slot also.
		return timetable


class Schedule():
	#courses is a dictionary as class -> list_of_list[subject,frequency,instructor].
	#days->time_slots->courses
	#list->list->list
	#assuming all classes have move more than 5 events per week.
	def __init__(self, time_slots, days, classes):
		self.time_slots = time_slots
		self.days = days 
		self.classes = classes
		self.timetable = make_timetable(time_slots, days, classes)
	

	def evaluate_coinciding_lectures(self):
		for i in self.timetable:
			# i === day		
			for j in i:
				# j == time_slot
				container = []
				for k in j:
					# k === [class, subject, instructor]
					if k[0] not in container:
						container.append(k[0])
					if k in container:
						return False
		return True

	def evaluate_coinciding_instructors(self):
		for i in self.timetable:
			container = []
			# j == time->courses dictionary
			for j in i:
				slots_courses = [[s,v] for s,v in j.items()]
				for k in slots_courses:
					entry = [k[0],k[1][2]]
					if entry not in container:
						container.append(entry)
					else:
						return False
		return True

	def same_subject_not_more_than_once(self):
		for i in self.timetable:
			container = []
			for j in i:
				slots_courses = [[s,v] for s,v in j.items]
				for k in slots_courses:
					entry = [k[0],k[1][0],k[1][1]]
					if entry not in container:
						container.append(entry)
					else:
						return False
		return True
#WE CANNOT CALL SELF.TIMETABLE IN EVALUATION METHODS SINCE IT WILL CREATE A RANDOM TIMETABLE AND THEN CHECK FOR IT.

	def instructor_rest():
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
			if(self.evaluate_coinciding_lectures):
				fitness += 0.3
			if(self.evaluate_coinciding_instructors):
				fitness += 0.3
			if(self.same_subject_not_more_than_once):
				fitness += 0.2
			if(self.instructor_rest):
				fitness += 0.2


class GeneticAlgorithm:
	def population(self, chromosomes = 50):
		return [Schedule().timetable for x in range(chromosomes)]

