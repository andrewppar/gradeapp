# Dependencies for the app

import Tkinter
import sys
import pickle
import tkMessageBox


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import *
import matplotlib.pyplot as plt

#Info for the Student Class. This way of doing things makes it impossible to customize the grade values within
#the app. Perhaps there is a way to accomplish this, but I can't think of a way now. 

A_plus = ['A+','A+|'] 
A = ['A', 'A |']			
A_minus = ['A-','A-|']
B_plus = ['B+', 'B+|']
B = ['B','B |']
B_minus = ['B-','B-|']
C_plus = ['C+', 'C+|']
C = ['C','C |']
C_minus = ['C-','C-|']
D_plus = ['D+', 'D+|']
D = ['D','D |']
D_minus = ['D-','D-|']
F = ['F','F |']

students = []


def average(lst):
	add = 0 
	for x in lst:
		add = add + x
	b = float(str(len(lst))+'.0')
	return add / b

def letter_grade(var):
	if var == 'N/A':
		return 'N/A' 
	elif float(var)< 60: 
		return 'F'
	elif float(var) >= 60 and float(var)<63: 
		return 'D-'
	elif float(var) >= 63  and float(var)<67: 
		return 'D'
	elif float(var) >= 67 and float(var)<70: 
		return 'D+'
	elif float(var) >= 70 and float(var)< 73: 
		return 'C-'
	elif float(var) >= 73 and float(var)< 77: 
		return 'C'
	elif float(var) >= 77 and float(var)<80: 
		return 'C+'
	elif float(var) >= 80 and float(var)< 83: 
		return 'B-'
	elif float(var) >= 83 and float(var)<86: 
		return 'B'
	elif float(var) >= 86 and float(var)<90: 
		return 'B+'
	elif float(var) >= 90 and float(var)< 93: 
		return 'A-'
	elif float(var) >= 93 and float(var)<96: 
		return 'A'
	elif float(var) >= 96 and float(var)<100: 
		return 'A+'
	elif float(var) >= 100:
		return 'A+'
	else:
		return 'Whoops'

class Student(object): 
	def __init__(self, name, quiz_1, quiz_2, quiz_3, quiz_4, quiz_5, quiz_6, midterm, final, participation):
		self.name = name
		self.quiz_1 = quiz_1
		self.quiz_2 = quiz_2
		self.quiz_3 = quiz_3
		self.quiz_4 = quiz_4
		self.quiz_5 = quiz_5
		self.quiz_6 = quiz_6
		self.midterm = midterm
		self.final = final 
		self.participation = participation
		
	def quiz_grade(self):
			if self.quiz_1 == 'N/A' or self.quiz_2 == 'N/A' or self.quiz_3 == 'N/A' or self.quiz_4 == 'N/A' or self.quiz_5 == 'N/A' or self.quiz_6 == 'N/A':
				return 'N/A'
			else: 
				quizzes = [int(self.quiz_1),int(self.quiz_2),int(self.quiz_3),int(self.quiz_4),int(self.quiz_5),int(self.quiz_6)]
				quizzes.sort()
				quiz_sum = 0 
				for x in range(1,6):
					quiz_sum = quiz_sum + quizzes[x]
				return quiz_sum / 5.0


	def final_grade(self):
		if self.quiz_grade() == 'N/A' or self.midterm == 'N/A' or self.final == 'N/A' or self.participation == 'N/A':
				return 'N/A'
		else: 
			return (float(self.quiz_grade()) * 0.25) + (float(self.midterm) * 0.30) + (float(self.final) * 0.30) + (float(self.participation) * 0.15)

students = []


#Class Pane 

class ClassPane(Tkinter.Tk):
	def __init__(self, parent, pupils):
		Tkinter.Tk.__init__(self, parent)
		self.info = pupils
		self.parent = parent
		self.initialize()

	def initialize(self): 
		a = self.info.replace(' ', '_')
		self.students = pickle.load(open( "save."+str(a), "rb" ))

		self.mainframe = Tkinter.Frame(self)
		self.mainframe.pack()


		self.frame  = Tkinter.LabelFrame(self.mainframe,font=("Helvetica", 10), text = "Roster", padx = 5, pady = 5)
		self.frame.grid(row = 0, column = 0, rowspan = 4)


		count = 0 
		ccount = 0
		for x in self.students:
			if count == 10: 
				ccount = ccount +1
				count = 0
			self.label = Tkinter.Label(self.frame,font=("Helvetica", 10), text = str(self.students.index(x)+1) +' '+ str(x.name), anchor = 'w')
			self.label.grid(row = count, column = ccount)
			count = count+1

		self.button1 = Tkinter.Button(self.mainframe,font=("Helvetica", 10), text = "Display Grades",command = self.display_class_grades)
		self.button1.grid(row=0,column =1,sticky = 'w'+'e'+'n'+'s')

		self.button4 = Tkinter.Button(self.mainframe,font=("Helvetica", 10), text = "Add Class Grade", command=self.add_class_grades)
		self.button4.grid(row = 1, column = 1,sticky = 'w'+'e'+'n'+'s')

		self.button2 = Tkinter.Button(self.mainframe,font=("Helvetica", 10), text = "Finalize Class", command=self.finish_class)
		self.button2.grid(row = 2,column = 1,sticky = 'w'+'e'+'n'+'s')

		self.button5 = Tkinter.Button(self.mainframe,font=("Helvetica", 10), text = "Save Changes", command = self.save_changes)
		self.button5.grid(row = 3, column = 1, sticky = 'w'+'e'+'n'+'s')


	def save_changes(self): 
		check = tkMessageBox.askquestion('Save', 'Are you sure you want to save changes to '+ str(self.info), icon = 'warning')
		if check == 'yes':
			a = self.info.replace(' ', '_')	
			pickle.dump( self.students, open( "save."+str(a), "wb" ) )

	def display_class_grades(self): 
		new_window = DisplayClassGrades(None, self.students)
		new_window.title("Class Averages")

	def add_class_grades(self):
		new_window = AddClassGrade(None, self.students)
		new_window.title("Add New Grade")

	def finish_class(self):
		for x in self.students: 
			if x.quiz_1 == 'N/A':
				new_window = AddAssessment(None, "Quiz 1", x)
				new_window.title("Add Quiz 1 for "+x.name)
			if x.quiz_2 == 'N/A':
				new_window = AddAssessment(None, "Quiz 2", x)
				new_window.title("Add Quiz 2 for "+x.name)

			if x.quiz_3 == 'N/A':
				new_window = AddAssessment(None, "Quiz 3", x)
				new_window.title("Add Quiz 3 for "+x.name)

			if x.quiz_4 == 'N/A':
				new_window = AddAssessment(None, "Quiz 4", x)
				new_window.title("Add Quiz 4 for "+x.name)

			if x.quiz_5 == 'N/A':
				new_window = AddAssessment(None, "Quiz 5", x)
				new_window.title("Add Quiz 5 for "+x.name)

			if x.quiz_6 == 'N/A':
				new_window = AddAssessment(None, "Quiz 6", x)
				new_window.title("Add Quiz 6 for "+x.name)

			if x.midterm == 'N/A':
				new_window = AddAssessment(None, "Midterm", x)
				new_window.title("Add Midterm for "+x.name)

			if x.final == 'N/A':
				new_window = AddAssessment(None, "Final", x)
				new_window.title("Add Final for "+x.name)

			if x.participation == 'N/A':
				new_window = AddAssessment(None, "Participation", x)
				new_window.title("Add Participation for "+x.name)


#Add Class Grade: Class Pane

class AddClassGrade(Tkinter.Toplevel): 
	def __init__(self,parent,students):
		Tkinter.Toplevel.__init__(self, parent)
		self.students = students
		self.parent = parent
		self.initialize()

	def initialize(self):
		

		self.label = Tkinter.LabelFrame(self,font=("Helvetica", 10), text = "Select Assessment")
		self.label.grid(row=0,column=0)

		self.buttonq1 = Tkinter.Button(self.label,font=("Helvetica", 10), text = "Quiz 1", command = lambda: self.press_quiz_1("Quiz 1"))
		self.buttonq1.grid(row = 0, column = 0, sticky = 'w'+'e'+'n'+'s')

		self.buttonq2 = Tkinter.Button(self.label,font=("Helvetica", 10), text = "Quiz 2", command = lambda: self.press_quiz_1("Quiz 2"))
		self.buttonq2.grid(row = 0, column = 1, sticky = 'w'+'e'+'n'+'s')

		self.buttonq3 = Tkinter.Button(self.label,font=("Helvetica", 10), text = "Quiz 3", command = lambda: self.press_quiz_1("Quiz 3"))
		self.buttonq3.grid(row = 0, column = 2, sticky = 'w'+'e'+'n'+'s')

		self.buttonq4 = Tkinter.Button(self.label,font=("Helvetica", 10), text = "Quiz 4", command = lambda: self.press_quiz_1("Quiz 4"))
		self.buttonq4.grid(row = 1, column = 0, sticky = 'w'+'e'+'n'+'s')

		self.buttonq5 = Tkinter.Button(self.label,font=("Helvetica", 10), text = "Quiz 5", command = lambda: self.press_quiz_1("Quiz 5"))
		self.buttonq5.grid(row = 1, column = 1, sticky = 'w'+'e'+'n'+'s')

		self.buttonq6 = Tkinter.Button(self.label,font=("Helvetica", 10), text = "Quiz 6", command = lambda: self.press_quiz_1("Quiz 6"))
		self.buttonq6.grid(row = 1, column = 2, sticky = 'w'+'e'+'n'+'s')


		self.buttonmid = Tkinter.Button(self.label,font=("Helvetica", 10), text = "Midterm",command = lambda: self.press_quiz_1("Midterm"))
		self.buttonmid.grid(row = 2, column = 0, sticky = 'w'+'e'+'n'+'s')

		self.buttonfin = Tkinter.Button(self.label,font=("Helvetica", 10), text = "Final",command = lambda: self.press_quiz_1("Final"))
		self.buttonfin.grid(row = 2, column = 1, sticky = 'w'+'e'+'n'+'s')

		self.buttonpart = Tkinter.Button(self.label,font=("Helvetica", 10), text = "Participation",command = lambda: self.press_quiz_1("Participation"))
		self.buttonpart.grid(row = 2, column = 2, sticky = 'w'+'e'+'n'+'s')

	def press_quiz_1(self,assess): 
		for x in self.students: 
			new_window = AddAssessment(None, assess, x)
			new_window.title("Add "+assess+" for "+x.name)
		self.destroy()



#Add Student and Assessment Grade
class AddAssessment(Tkinter.Toplevel):
	def __init__(self, parent,assess, student):
		Tkinter.Toplevel.__init__(self, parent)
		self.assess = assess
		self.student = student
		self.parent = parent
		self.initialize()


	def initialize(self):
		self.label = Tkinter.LabelFrame(self,font=("Helvetica", 10), text = self.student.name)
		self.label.grid(row=0,column=0)

		self.label1 = Tkinter.Label(self.label,font=("Helvetica", 10), text = self.assess+": ")
		self.label1.grid(row = 0, column = 0)

		self.entryvar1 = Tkinter.StringVar()
		self.entryvar1 = Tkinter.Entry(self.label,font=("Helvetica", 10), textvariable = self.entryvar1)
		self.entryvar1.focus_set()
		self.entryvar1.grid(row = 0, column = 1)
		self.entryvar1.bind('<Return>', self.Eenter_grade)

		self.button = Tkinter.Button(self,font=("Helvetica", 10), text = "Enter Grade",command = self.enter_grade)
		self.button.grid(row = 1, column = 0, columnspan = 2)

	def Eenter_grade(self, event):
		grade = self.entryvar1.get()
		if not grade.isdigit(): 
			error =  tkMessageBox.showinfo("Error", "You must enter a grade for "+self.student.name)
		else: 
			if self.assess == "Quiz 1": 
				self.student.quiz_1 = int(grade)
				self.destroy()

			elif self.assess == "Quiz 2": 
				self.student.quiz_2 = int(grade)
				self.destroy()

			elif self.assess == "Quiz 3": 
				self.student.quiz_3 = int(grade)
				self.destroy()

			elif self.assess == "Quiz 4": 
				self.student.quiz_4 = int(grade)
				self.destroy()

			elif self.assess == "Quiz 5": 
				self.student.quiz_5 = int(grade)
				self.destroy()

			elif self.assess == "Quiz 6": 
				self.student.quiz_6 = int(grade)
				self.destroy()

			elif self.assess == "Midterm": 
				self.student.midterm = int(grade)
				self.destroy()

			elif self.assess == "Final": 
				self.student.final = int(grade)
				self.destroy()

			elif self.assess == "Participation": 
				self.student.participation = int(grade)
				self.destroy()

	def enter_grade(self): 
		grade = self.entryvar1.get()
		if not grade.isdigit(): 
			error =  tkMessageBox.showinfo("Error", "You must enter a grade for "+self.student.name)
		else: 
			if self.assess == "Quiz 1": 
				self.student.quiz_1 = int(grade)
				self.destroy()

			elif self.assess == "Quiz 2": 
				self.student.quiz_2 = int(grade)
				self.destroy()

			elif self.assess == "Quiz 3": 
				self.student.quiz_3 = int(grade)
				self.destroy()

			elif self.assess == "Quiz 4": 
				self.student.quiz_4 = int(grade)
				self.destroy()

			elif self.assess == "Quiz 5": 
				self.student.quiz_5 = int(grade)
				self.destroy()

			elif self.assess == "Quiz 6": 
				self.student.quiz_6 = int(grade)
				self.destroy()

			elif self.assess == "Midterm": 
				self.student.midterm = int(grade)
				self.destroy()

			elif self.assess == "Final": 
				self.student.final = int(grade)
				self.destroy()

			elif self.assess == "Participation": 
				self.student.participation = int(grade)
				self.destroy()








# Display Grades : Class Pane 

class DisplayClassGrades(Tkinter.Toplevel):
	def __init__(self, parent,info):
		Tkinter.Toplevel.__init__(self, parent)
		self.info = info
		self.parent = parent
		self.initialize()


	def initialize(self):
		self.q1 = []
		for x in self.info: 
			if x.quiz_1 != 'N/A':
				self.q1.append(int(x.quiz_1))

		if self.q1 == []:
			q1avg = 'N/A'
		else: 
			q1avg = average(self.q1)

		self.q2 = []
		for x in self.info: 
			if x.quiz_2 != 'N/A':
				self.q2.append(int(x.quiz_2))
		if self.q2 == []:
			q2avg = 'N/A'
		else: 
			q2avg = average(self.q2)

		self.q3 = []
		for x in self.info: 
			if x.quiz_3 != 'N/A':
				self.q3.append(int(x.quiz_3))
		if self.q3 == []:
			q3avg = 'N/A'
		else: 
			q3avg = average(self.q3)

		self.q4 = []
		for x in self.info: 
			if x.quiz_4 != 'N/A':
				self.q4.append(int(x.quiz_4))
		if self.q4 == []:
			q4avg = 'N/A'
		else: 
			q4avg = average(self.q4)


		self.q5 = []
		for x in self.info: 
			if x.quiz_5 != 'N/A':
				self.q5.append(int(x.quiz_5))
		if self.q5 == []:
			q5avg = 'N/A'
		else: 
			q5avg = average(self.q5)


		self.q6 = []
		for x in self.info: 
			if x.quiz_6 != 'N/A':
				self.q6.append(int(x.quiz_6))
		if self.q6 == []:
			q6avg = 'N/A'
		else: 
			q6avg = average(self.q6)

		self.mid = []
		for x in self.info: 
			if x.midterm != 'N/A':
				self.mid.append(int(x.midterm))
		if self.mid == []:
			midavg = 'N/A'
		else: 
			midavg = average(self.mid)

		self.fin = []
		for x in self.info: 
			if x.final != 'N/A':
				self.fin.append(int(x.final))
		if self.fin == []:
			finavg = 'N/A'
		else: 
			finavg = average(self.fin)

		self.part = []
		for x in self.info: 
			if x.participation != 'N/A':
				self.part.append(int(x.participation))
		if self.part == []:
			partavg = 'N/A'
		else: 
			partavg = average(self.part)

		self.overall = []
		for x in self.info: 
			if x.final_grade() != 'N/A':
				self.overall.append(int(x.final_grade()))
		if self.overall == []:
			overallavg = 'N/A'
		else: 
			overallavg = average(self.overall)

		self.frame = Tkinter.LabelFrame(self,font=("Helvetica", 10), text = "Quiz Averages")
		self.frame.grid(row = 0, column = 0, columnspan = 3)
		
		self.q1lab = Tkinter.Label(self.frame,font=("Helvetica", 10), text = "Quiz 1: ")
		self.q1lab.grid(row = 0, column = 0)

		self.q1laba = Tkinter.Label(self.frame,font=("Helvetica", 10), text = str(q1avg))
		self.q1laba.grid(row = 0, column = 1)

		self.q1button = Tkinter.Button(self.frame,font=("Helvetica", 10), text = "Display Graph", command = self.quiz1graph)
		self.q1button.grid(row = 0, column = 3)

		self.q2lab = Tkinter.Label(self.frame,font=("Helvetica", 10), text = "Quiz 2: ")
		self.q2lab.grid(row = 1, column = 0)

		self.q2laba = Tkinter.Label(self.frame,font=("Helvetica", 10), text = str(q2avg))
		self.q2laba.grid(row = 1, column = 1)

		self.q2button = Tkinter.Button(self.frame,font=("Helvetica", 10), text = "Display Graph", command = self.quiz2graph)
		self.q2button.grid(row = 1, column = 3)
		
		self.q3lab = Tkinter.Label(self.frame,font=("Helvetica", 10), text = "Quiz 3: ")
		self.q3lab.grid(row = 2, column = 0)

		self.q3laba = Tkinter.Label(self.frame,font=("Helvetica", 10), text = str(q3avg))
		self.q3laba.grid(row = 2, column = 1)

		self.q3button = Tkinter.Button(self.frame,font=("Helvetica", 10), text = "Display Graph", command = self.quiz3graph)
		self.q3button.grid(row = 2, column = 3)

		self.q4lab = Tkinter.Label(self.frame,font=("Helvetica", 10), text = "Quiz 4: ")
		self.q4lab.grid(row = 3, column = 0)

		self.q4laba = Tkinter.Label(self.frame,font=("Helvetica", 10), text = str(q4avg))
		self.q4laba.grid(row = 3, column = 1)

		self.q4button = Tkinter.Button(self.frame,font=("Helvetica", 10), text = "Display Graph", command = self.quiz4graph)
		self.q4button.grid(row = 3, column = 3)
		
		self.q5lab = Tkinter.Label(self.frame,font=("Helvetica", 10), text = "Quiz 5: ")
		self.q5lab.grid(row = 4, column = 0)

		self.q5laba = Tkinter.Label(self.frame,font=("Helvetica", 10), text = str(q5avg))
		self.q5laba.grid(row = 4, column = 1)

		self.q5button = Tkinter.Button(self.frame,font=("Helvetica", 10), text = "Display Graph", command = self.quiz5graph)
		self.q5button.grid(row = 4, column = 3)
		
		self.q6lab = Tkinter.Label(self.frame,font=("Helvetica", 10), text = "Quiz 6: ")
		self.q6lab.grid(row = 5, column = 0)

		self.q6laba = Tkinter.Label(self.frame,font=("Helvetica", 10), text = str(q6avg))
		self.q6laba.grid(row = 5, column = 1)

		self.q6button = Tkinter.Button(self.frame,font=("Helvetica", 10), text = "Display Graph", command = self.quiz6graph)
		self.q6button.grid(row = 5, column = 3)
		
		self.frame2 = Tkinter.LabelFrame(self,font=("Helvetica", 10), text = "Exam & Participation Averages")
		self.frame2.grid(row = 1, column = 0, columnspan = 3)

		self.midlab = Tkinter.Label(self.frame2,font=("Helvetica", 10), text = "Midterm Exam: ")
		self.midlab.grid(row = 0, column = 0)

		self.midlaba = Tkinter.Label(self.frame2,font=("Helvetica", 10), text = str(midavg))
		self.midlaba.grid(row = 0, column = 1)

		self.midbutton = Tkinter.Button(self.frame2,font=("Helvetica", 10), text = "Display Graph", command = self.midgraph)
		self.midbutton.grid(row = 0, column = 3)
		
		self.finlab = Tkinter.Label(self.frame2,font=("Helvetica", 10), text = "Final Exam: ")
		self.finlab.grid(row = 1, column = 0)

		self.finlaba = Tkinter.Label(self.frame2,font=("Helvetica", 10), text = str(finavg))
		self.finlaba.grid(row = 1, column = 1)

		self.finbutton = Tkinter.Button(self.frame2,font=("Helvetica", 10), text = "Display Graph", command = self.fingraph)
		self.finbutton.grid(row = 1, column = 3)
		
		self.partlab = Tkinter.Label(self.frame2,font=("Helvetica", 10), text = "Participation: ")
		self.partlab.grid(row = 2, column = 0)

		self.partlaba = Tkinter.Label(self.frame2,font=("Helvetica", 10), text = str(partavg))
		self.partlaba.grid(row = 2, column = 1)

		self.partbutton = Tkinter.Button(self.frame2,font=("Helvetica", 10), text = "Display Graph", command = self.partgraph)
		self.partbutton.grid(row = 2, column = 3)
		
		self.overalllab = Tkinter.Label(self,font=("Helvetica", 10), text = "Final Grade Average: ")
		self.overalllab.grid(row = 2, column = 0)

		self.overalllaba = Tkinter.Label(self,font=("Helvetica", 10), text = str(overallavg))
		self.overalllaba.grid(row = 2, column = 1)

		self.overallbutton = Tkinter.Button(self,font=("Helvetica", 10), text = "Display Graph", command = self.overallgraph)
		self.overallbutton.grid(row = 2, column = 2)

	def quiz1graph(self):
		if self.q1 != []:
			new_window = ClassGraphAverage(None, self.q1, self.info, "Quiz 1")
			new_window.title("Quiz 1 Data") 
		else: 
			error = tkMessageBox.showinfo('Error', 'There is no Quiz 1 data to graph. ')

	def quiz2graph(self):
		if self.q2 != []:
			new_window = ClassGraphAverage(None, self.q2, self.info, "Quiz 2")
			new_window.title("Quiz 2 Data") 
		else: 
			error = tkMessageBox.showinfo('Error', 'There is no Quiz 2 data to graph. ')
	def quiz3graph(self):
		if self.q3 != []:
			new_window = ClassGraphAverage(None, self.q3,self.info, "Quiz 3")
			new_window.title("Quiz 3 Data") 
		else: 
			error = tkMessageBox.showinfo('Error', 'There is no Quiz 3 data to graph. ')
	def quiz4graph(self):
		if self.q4 != []:
			new_window = ClassGraphAverage(None, self.q4,self.info, "Quiz 4")
			new_window.title("Quiz 4 Data") 
		else: 
			error = tkMessageBox.showinfo('Error', 'There is no Quiz 4 data to graph. ')
	def quiz5graph(self):
		if self.q5 != []:
			new_window = ClassGraphAverage(None, self.q5,self.info, "Quiz 5")
			new_window.title("Quiz 5 Data") 
		else: 
			error = tkMessageBox.showinfo('Error', 'There is no Quiz 5 data to graph. ')
	def quiz6graph(self):
		if self.q6 != []:
			new_window = ClassGraphAverage(None, self.q6,self.info, "Quiz 6")
			new_window.title("Quiz 6 Data") 
		else: 
			error = tkMessageBox.showinfo('Error', 'There is no Quiz 6 data to graph. ')
	def midgraph(self):
		if self.mid != []:
			new_window = ClassGraphAverage(None, self.mid,self.info, "Midterm")
			new_window.title("Midterm Exam Data") 
		else: 
			error = tkMessageBox.showinfo('Error', 'There is no Midterm data to graph. ')
	def fingraph(self):
		if self.fin != []:
			new_window = ClassGraphAverage(None, self.fin,self.info, "Final")
			new_window.title("Final Exam Data") 
		else: 
			error = tkMessageBox.showinfo('Error', 'There is no Final Exam data to graph. ')
	def partgraph(self):
		if self.part != []:
			new_window = ClassGraphAverage(None, self.part,self.info, "Participation")
			new_window.title("Participation Data")
		else: 
			error = tkMessageBox.showinfo('Error', 'There is no Participation data to graph. ')
	def overallgraph(self):
		if self.overall != []:
			new_window = ClassGraphAverage(None, self.overall,self.info, "Overall")
			new_window.title("Final Grade Data") 
		else: 
			error = tkMessageBox.showinfo('Error', 'There is no Final Grade data to graph. ')

# Graph for Student Data : Display Grades : Class Pane 

class ClassGraphAverage(Tkinter.Toplevel):
	def __init__(self,parent, info, students, assess):
		Tkinter.Toplevel.__init__(self,parent)
		self.parent = parent
		self.info = info
		self.assess = assess
		self.students = students
		self.initialize()

	def initialize(self):
		if self.assess == "Quiz 1": 
			count = 1 
			for x in self.students: 
				self.label = Tkinter.Label(self,font=("Helvetica", 10), text = x.name+": "+str(x.quiz_1))
				self.label.grid(row = count, column = 0)
				count = count + 1 

		elif self.assess == "Quiz 2": 
			count = 1 
			for x in self.students: 
				self.label = Tkinter.Label(self,font=("Helvetica", 10), text = x.name+": "+str(x.quiz_2))
				self.label.grid(row = count, column = 0)
				count = count + 1 

		elif self.assess == "Quiz 3": 
			count = 1 
			for x in self.students: 
				self.label = Tkinter.Label(self,font=("Helvetica", 10), text = x.name+": "+str(x.quiz_3))
				self.label.grid(row = count, column = 0)
				count = count + 1 

		elif self.assess == "Quiz 4": 
			count = 1 
			for x in self.students: 
				self.label = Tkinter.Label(self,font=("Helvetica", 10), text = x.name+": "+str(x.quiz_4))
				self.label.grid(row = count, column = 0)
				count = count + 1 

		elif self.assess == "Quiz 5": 
			count = 1 
			for x in self.students: 
				self.label = Tkinter.Label(self,font=("Helvetica", 10), text = x.name+": "+str(x.quiz_5))
				self.label.grid(row = count, column = 0)
				count = count + 1 

		elif self.assess == "Quiz 6": 
			count = 1 
			for x in self.students: 
				self.label = Tkinter.Label(self,font=("Helvetica", 10), text = x.name+": "+str(x.quiz_6))
				self.label.grid(row = count, column = 0)
				count = count + 1 

		elif self.assess == "Midterm": 
			count = 1 
			for x in self.students: 
				self.label = Tkinter.Label(self,font=("Helvetica", 10), text = x.name+": "+str(x.midterm))
				self.label.grid(row = count, column = 0)
				count = count + 1 

		elif self.assess == "Final": 
			count = 1 
			for x in self.students: 
				self.label = Tkinter.Label(self,font=("Helvetica", 10), text = x.name+": "+str(x.final))
				self.label.grid(row = count, column = 0)
				count = count + 1 

		elif self.assess == "Participation": 
			count = 1 
			for x in self.students: 
				self.label = Tkinter.Label(self,font=("Helvetica", 10), text = x.name+": "+str(x.participation))
				self.label.grid(row = count, column = 0)
				count = count + 1 
		elif self.assess == "Overall":
			count = 1 
			for x in self.students:
				fin = x.final_grade() 
				self.label = Tkinter.Label(self,font=("Helvetica", 10), text = x.name+": "+str(fin))
				self.label.grid(row = count, column = 0)
				count = count + 1

		frame = Tkinter.Frame(self)
		
		a = average(self.info)

		self.labelnum2 = Tkinter.Label(self, text = 'Average: ', anchor = 'w', font=("Helvetica", 20))
		self.labelnum2.grid(column = 0, row = count +1)

		self.label2 = Tkinter.Label(self, text = str(a), anchor = 'w',font=("Helvetica", 20))
		self.label2.grid(column = 1, row = count+ 1)

		dct = {'A+':0, 'A':0, 'A-':0, 'B+':0,'B':0,'B-':0, 'C+':0,'C':0,'C-':0, 'D+':0,'D':0,'D-':0, 'F':0}
		for x in self.info: 
			dct[letter_grade(x)] = dct[letter_grade(x)]+1
		
		fig=plt.figure()
		ax=fig.add_subplot(111)

		grds=['A+', 'A', 'A-', 'B+','B','B-', 'C+','C','C-', 'D+','D','D-', 'F']
		N=len(grds)
		ind=np.arange(N)
		width=1
		list_a=(dct['A+'],dct['A'],dct['A-'],dct['B+'],dct['B'],dct['B-'],dct['C+'],dct['C'],dct['C-'],dct['D+'],dct['D'],dct['D-'], dct['F'])
		x=np.arange(N)
		ax.set_xlabel('Grades')
		ax.set_ylabel('Number of Students')
		ax.set_ylim(0,10)
		ax.set_xticks(ind+width)
		ax.set_xticklabels(grds,rotation='vertical')
		rects1=ax.bar(ind,list_a,width,color='b')
		
		ax.grid(True)
		self.canvas = FigureCanvasTkAgg(fig,master=self)
		self.canvas.show()
		self.canvas.get_tk_widget().grid(row =0, column = 2, rowspan = count)

		frame.grid(row =0, column = 0 )

#Student Pane 

class StudentPane(Tkinter.Tk):
	def __init__(self, parent,pupils):
		Tkinter.Tk.__init__(self, parent)
		self.info = pupils
		self.parent = parent
		self.initialize()

	def initialize(self):



		a = self.info.replace(' ', '_')
		self.students = pickle.load(open( "save."+str(a), "rb" ))

		self.mainframe = Tkinter.Frame(self)
		self.mainframe.pack()


		self.frame  = Tkinter.LabelFrame(self.mainframe,font=("Helvetica", 10), text = "Roster", padx = 5, pady = 5)
		self.frame.grid(row = 0, column = 0, rowspan = 5)

		self.list = Tkinter.Listbox(self.frame,font=("Helvetica", 10))
		self.list.grid(row = 0, column = 0)

		for x in self.students: 
			self.list.insert('end',str(x.name)) 

		self.button1 = Tkinter.Button(self.mainframe,font=("Helvetica", 10), text = "Display Grade", command = self.display_grade)
		self.button1.grid(row=0,column =1,sticky = 'w'+'e'+'n'+'s')

		self.button2 = Tkinter.Button(self.mainframe,font=("Helvetica", 10), text = "Calculate Grade", command = self.calculate_grade)
		self.button2.grid(row=1,column = 1,sticky = 'w'+'e'+'n'+'s')

		self.button3 = Tkinter.Button(self.mainframe,font=("Helvetica", 10), text = "Add One Grade", command = self.add_one_grade)
		self.button3.grid(row =2, column =1,sticky = 'w'+'e'+'n'+'s')

		self.button4 = Tkinter.Button(self.mainframe,font=("Helvetica", 10), text = "Add All Grades", command = self.add_all_grades)
		self.button4.grid(row = 3, column = 1,sticky = 'w'+'e'+'n'+'s')

		self.button6 = Tkinter.Button(self.mainframe,font=("Helvetica", 10), text = "Finish Grades", command = self.finish_grade)
		self.button6.grid(row = 4, column = 1, sticky = 'w'+'e'+'n'+'s')

		self.button5 = Tkinter.Button(self.mainframe,font=("Helvetica", 10), text = "Save Changes", command = self.save_changes)
		self.button5.grid(row = 5, column = 0, columnspan = 2, sticky = 'w'+'e'+'n'+'s')

	def display_grade(self): 
		if self.list.curselection() == (): 
			error = tkMessageBox.showinfo('Error', 'You must select a student')

		else: 
			i = self.list.curselection()[0]
			t = self.list.get(i)
			s = ''
			for x in self.students:
				  
				if x.name == t: 
					s = x
			
			new_window = DisplayGrade(None,s)
			new_window.title(s.name +" Grades")

	def calculate_grade(self):
		if self.list.curselection() == (): 
			error = tkMessageBox.showinfo('Error', 'You must select a student')

		else: 
			i = self.list.curselection()[0]
			t = self.list.get(i)
			s = ''
			for x in self.students:
				  
				if x.name == t: 
					s = x
			
			new_window = CalculateGrade(None,s)
			new_window.title(s.name +" Grades")

	def add_one_grade(self):
		if self.list.curselection() == (): 
			error = tkMessageBox.showinfo('Error', 'You must select a student')

		else: 
			i = self.list.curselection()[0]
			t = self.list.get(i)
			s = ''
			for x in self.students:
				  
				if x.name == t: 
					s = x
			
			new_window = AddOneGrade(None,s)
			new_window.title("Add Grade for " + s.name)

	def add_all_grades(self):
		if self.list.curselection() == (): 
			error = tkMessageBox.showinfo('Error', 'You must select a student')

		else: 
			i = self.list.curselection()[0]
			t = self.list.get(i)
			s = ''
			for x in self.students:
				  
				if x.name == t: 
					s = x
		new_window = AddAllGrades(None, s)
		new_window.title("Add All Grades for "+ s.name)

	def save_changes(self): 
		check = tkMessageBox.askquestion('Save', 'Are you sure you want to save changes to '+ str(self.info), icon = 'warning')
		if check == 'yes':
			a = self.info.replace(' ', '_')	
			pickle.dump( self.students, open( "save."+str(a), "wb" ) )

	def finish_grade(self):

		if self.list.curselection() == (): 
			error = tkMessageBox.showinfo('Error', 'You must select a student')

		else: 
			i = self.list.curselection()[0]
			t = self.list.get(i)
			s = ''
			for x in self.students:
				  
				if x.name == t: 
					s = x
			
			new_window = FinishGrade(None,s)
			new_window.title(s.name +" Grades")

#Display Grade : Student Pane 

class DisplayGrade(Tkinter.Toplevel):
	def __init__(self, parent,info):
		Tkinter.Toplevel.__init__(self, parent)
		self.info = info
		self.parent = parent
		self.initialize()

	def initialize(self):
		self.lframe1 = Tkinter.LabelFrame(self,font=("Helvetica", 10), text = "Scores", padx = 5, pady = 5)
		self.lframe1.grid(row = 0, column = 0)


		self.lframe2 = Tkinter.LabelFrame(self,font=("Helvetica", 10), text = "Grade", padx = 5, pady = 5)
		self.lframe2.grid(row = 1, column = 0)

		self.labela1 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = "Quiz 1: ")
		self.labela1.grid(row=0, column =0)

		self.labelb1 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = "Quiz 2: ")
		self.labelb1.grid(row=1, column =0)

		self.labelc1 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = "Quiz 3: ")
		self.labelc1.grid(row=2, column =0)

		self.labeld1 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = "Quiz 4: ")
		self.labeld1.grid(row=3, column =0)

		self.labele1 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = "Quiz 5: ")
		self.labele1.grid(row=4, column =0)

		self.labelf1 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = "Quiz 6: ")
		self.labelf1.grid(row=5, column =0)

		self.labelg1 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = "Midterm Exam: ")
		self.labelg1.grid(row=6, column =0)

		self.labelh1 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = "Final Exam: ")
		self.labelh1.grid(row=7, column =0)

		self.labeli1 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = "Participation: ")
		self.labeli1.grid(row=8, column =0)

		self.labelj1 = Tkinter.Label(self.lframe2,font=("Helvetica", 10), text = "Final Grade: ")
		self.labelj1.grid(row=0, column =0)

		self.labela2 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = self.info.quiz_1)
		self.labela2.grid(row=0, column =1)

		self.labelb2 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = self.info.quiz_2)
		self.labelb2.grid(row=1, column =1)

		self.labelb3 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = self.info.quiz_3)
		self.labelb3.grid(row=2, column =1)

		self.labelb4 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = self.info.quiz_4)
		self.labelb4.grid(row=3, column =1)

		self.labelc2 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = self.info.quiz_5)
		self.labelc2.grid(row=4, column =1)

		self.labeld2 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = self.info.quiz_6)
		self.labeld2.grid(row=5, column =1)

		self.labele2 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = self.info.midterm)
		self.labele2.grid(row=6, column =1)

		self.labelf2 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = self.info.final)
		self.labelf2.grid(row=7, column =1)

		self.labelg2 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = self.info.participation)
		self.labelg2.grid(row=8, column =1)

		self.labelh2 = Tkinter.Label(self.lframe2,font=("Helvetica", 10), text = self.info.final_grade())
		self.labelh2.grid(row = 0, column = 1)

#Calculate Grade : Student Pane

class CalculateGrade(Tkinter.Toplevel):
	def __init__(self, parent,info):
		Tkinter.Toplevel.__init__(self, parent)
		self.info = info
		self.parent = parent
		self.initialize()

	def initialize(self):

		
		self.lframe1 = Tkinter.LabelFrame(self,font=("Helvetica", 10), text = "Scores", padx = 5, pady = 5)
		self.lframe1.grid(row = 0, column = 0)

		self.button = Tkinter.Button(self,font=("Helvetica", 10), text = "Calculate", command = self.calcgrade)
		self.button.grid(row = 1, column =0 )
		self.lframe2 = Tkinter.LabelFrame(self,font=("Helvetica", 10), text = "Grade", padx = 5, pady = 5)
		self.lframe2.grid(row = 2, column = 0)

		 
		self.labela1 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = "Quiz 1: ")
		self.labela1.grid(row=0, column =0)

		self.labelb1 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = "Quiz 2: ")
		self.labelb1.grid(row=1, column =0)

		self.labelc1 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = "Quiz 3: ")
		self.labelc1.grid(row=2, column =0)

		self.labeld1 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = "Quiz 4: ")
		self.labeld1.grid(row=3, column =0)

		self.labele1 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = "Quiz 5: ")
		self.labele1.grid(row=4, column =0)

		self.labelf1 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = "Quiz 6: ")
		self.labelf1.grid(row=5, column =0)

		self.labelg1 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = "Midterm Exam: ")
		self.labelg1.grid(row=6, column =0)

		self.labelh1 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = "Final Exam: ")
		self.labelh1.grid(row=7, column =0)

		self.labeli1 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = "Participation: ")
		self.labeli1.grid(row=8, column =0)

		self.labelj1 = Tkinter.Label(self.lframe2,font=("Helvetica", 10), text = "Final Grade: ")
		self.labelj1.grid(row=0, column =0)

		self.q1check = True
		if self.info.quiz_1 == 'N/A':
			self.entryvar1 = Tkinter.StringVar()
			self.entryvar1 = Tkinter.Entry(self.lframe1,font=("Helvetica", 10), textvariable = self.entryvar1)
			self.entryvar1.grid(row = 0, column = 1)
			self.q1check = False
		else: 	
			self.labela2 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = self.info.quiz_1)
			self.labela2.grid(row=0, column =1)

		self.q2check = True
		if self.info.quiz_2 == 'N/A':
			self.entryvar2 = Tkinter.StringVar()
			self.entryvar2 = Tkinter.Entry(self.lframe1,font=("Helvetica", 10), textvariable = self.entryvar2)
			self.entryvar2.grid(row = 1, column = 1)
			self.q2check = False
		else: 	
			self.labelb2 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = self.info.quiz_2)
			self.labelb2.grid(row=1, column =1)

		
		self.q3check = True
		if self.info.quiz_3 == 'N/A':
			self.entryvar3 = Tkinter.StringVar()
			self.entryvar3 = Tkinter.Entry(self.lframe1,font=("Helvetica", 10), textvariable = self.entryvar3)
			self.entryvar3.grid(row = 2, column = 1)
			self.q3check = False
		else: 	
			self.labelb3 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = self.info.quiz_3)
			self.labelb3.grid(row=2, column =1)
		

		self.q4check = True
		if self.info.quiz_4 == 'N/A':
			self.entryvar4 = Tkinter.StringVar()
			self.entryvar4 = Tkinter.Entry(self.lframe1,font=("Helvetica", 10), textvariable = self.entryvar4)
			self.entryvar4.grid(row = 3, column = 1)
			self.q4check = False
		else: 	
			self.labelb3 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = self.info.quiz_4)
			self.labelb3.grid(row=3, column =1)

		self.q5check = True
		if self.info.quiz_5 == 'N/A':
			self.entryvar5 = Tkinter.StringVar()
			self.entryvar5 = Tkinter.Entry(self.lframe1,font=("Helvetica", 10), textvariable = self.entryvar5)
			self.entryvar5.grid(row = 4, column = 1)
			self.q5check = False
		else: 	
			self.labelb4 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = self.info.quiz_5)
			self.labelb4.grid(row=4, column =1)

		self.q6check = True
		if self.info.quiz_6 == 'N/A':
			self.entryvar6 = Tkinter.StringVar()
			self.entryvar6 = Tkinter.Entry(self.lframe1,font=("Helvetica", 10), textvariable = self.entryvar6)
			self.entryvar6.grid(row = 5, column = 1)
			self.q6check = False
		else: 	
			self.labelc2 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = self.info.quiz_6)
			self.labelc2.grid(row= 5, column =1)


		self.midcheck = True
		if self.info.midterm == 'N/A':
			self.entryvarm = Tkinter.StringVar()
			self.entryvarm = Tkinter.Entry(self.lframe1,font=("Helvetica", 10), textvariable = self.entryvarm)
			self.entryvarm.grid(row = 6, column = 1)
			self.midcheck = False
		else: 	
			self.labele2 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = self.info.midterm)
			self.labele2.grid(row=6, column =1)
		

		self.fincheck = True
		if self.info.final == 'N/A':
			self.entryvarf = Tkinter.StringVar()
			self.entryvarf = Tkinter.Entry(self.lframe1,font=("Helvetica", 10), textvariable = self.entryvarf)
			self.entryvarf.grid(row = 7, column = 1)
			self.fincheck = False
		else: 	
			self.labele3 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = self.info.final)
			self.labele3.grid(row=7, column =1)
		

		self.parcheck = True
		if self.info.participation == 'N/A':
			self.entryvarp = Tkinter.StringVar()
			self.entryvarp = Tkinter.Entry(self.lframe1,font=("Helvetica", 10), textvariable = self.entryvarp)
			self.entryvarp.grid(row = 8, column = 1)
			self.parcheck = False
		else: 	
			self.labele4 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = self.info.participation)
			self.labele4.grid(row=8, column =1)
		
		self.myvar = Tkinter.StringVar()
		self.myvar.set(' ')
		self.labelh2 = Tkinter.Label(self.lframe2,font=("Helvetica", 10), textvariable = self.myvar)
		self.labelh2.grid(row = 0, column = 1)
		
				

	def calcgrade(self):
		a = Student('example','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A')
		
		if self.q1check: 
			a.quiz_1 = self.info.quiz_1
		else: 
			c = self.entryvar1.get()
			if not c.isdigit(): 
				error = tkMessageBox.showinfo('Error', 'The number of students must be a number')
			else:  
				a.quiz_1 = int(c)

		if self.q2check: 
			a.quiz_2 = self.info.quiz_2
		else: 
			c = self.entryvar2.get()
			if not c.isdigit(): 
				error = tkMessageBox.showinfo('Error', 'The number of students must be a number')
			else:  
				a.quiz_2 = int(c)

		if self.q3check: 
			a.quiz_3 = self.info.quiz_3
		else: 
			c = self.entryvar3.get()
			if not c.isdigit(): 
				error = tkMessageBox.showinfo('Error', 'The number of students must be a number')
			else:  
				a.quiz_3 = int(c)

		if self.q4check: 
			a.quiz_4 = self.info.quiz_4
		else: 
			c = self.entryvar4.get()
			if not c.isdigit(): 
				error = tkMessageBox.showinfo('Error', 'The number of students must be a number')
			else:  
				a.quiz_4 = int(c)

		if self.q5check: 
			a.quiz_5 = self.info.quiz_5
		else: 
			c = self.entryvar5.get()
			if not c.isdigit(): 
				error = tkMessageBox.showinfo('Error', 'The number of students must be a number')
			else:  
				a.quiz_5 = int(c)

		if self.q6check: 
			a.quiz_6 = self.info.quiz_6
		else: 
			c = self.entryvar6.get()
			if not c.isdigit(): 
				error = tkMessageBox.showinfo('Error', 'The number of students must be a number')
			else:  
				a.quiz_6 = int(c)

		if self.midcheck: 
			a.midterm = self.info.midterm
		else: 
			c = self.entryvarm.get()
			if not c.isdigit(): 
				error = tkMessageBox.showinfo('Error', 'The number of students must be a number')
			else:  
				a.midterm = int(c)

		if self.fincheck: 
			a.final = self.info.final
		else: 
			c = self.entryvarf.get()
			if not c.isdigit(): 
				error = tkMessageBox.showinfo('Error', 'The number of students must be a number')
			else:  
				a.final = int(c)

		if self.parcheck: 
			a.participation = self.info.participation
		else: 
			c = self.entryvarp.get()
			if not c.isdigit(): 
				error = tkMessageBox.showinfo('Error', 'The number of students must be a number')
			else:  
				a.participation = int(c)

		fin = a.final_grade()
		
		self.myvar.set(str(fin))


# Add One Grade : Student Pane (This allows one to select a grade to add and edit only that grade for the selected student.)
		

class AddOneGrade(Tkinter.Toplevel):
	def __init__(self, parent,info):
		Tkinter.Toplevel.__init__(self, parent)
		self.info = info
		self.parent = parent
		self.initialize()

	def initialize(self):
		self.mainframe = Tkinter.Frame(self)
		self.mainframe.grid(row=0, column = 0)

		self.assess = ''

		self.qlabel = Tkinter.LabelFrame(self.mainframe,font=("Helvetica", 10), text = "Quizzes")
		self.qlabel.grid(row = 0, column = 0)
		self.b1 = Tkinter.Button(self.qlabel,font=("Helvetica", 10), text = "Quiz 1",command = self.press_q1)
		self.b1.grid(row= 0, column = 0)

		self.b2 = Tkinter.Button(self.qlabel,font=("Helvetica", 10), text = "Quiz 2", command = self.press_q2)
		self.b2.grid(row= 1, column = 0)

		self.b3 = Tkinter.Button(self.qlabel,font=("Helvetica", 10), text = "Quiz 3", command = self.press_q3)
		self.b3.grid(row= 2, column = 0)

		self.b4 = Tkinter.Button(self.qlabel,font=("Helvetica", 10), text = "Quiz 4", command = self.press_q4)
		self.b4.grid(row= 0, column = 1)

		self.b5 = Tkinter.Button(self.qlabel,font=("Helvetica", 10), text = "Quiz 5", command = self.press_q5)
		self.b5.grid(row= 1, column = 1)

		self.b6 = Tkinter.Button(self.qlabel,font=("Helvetica", 10), text = "Quiz 6", command = self.press_q6)
		self.b6.grid(row= 2, column = 1)

		self.elabel = Tkinter.LabelFrame(self.mainframe,font=("Helvetica", 10), text = "Exams")
		self.elabel.grid(row = 1, column = 0)
		self.bmid = Tkinter.Button(self.elabel,font=("Helvetica", 10), text = "Midterm", command = self.press_mid)
		self.bmid.grid(row= 0, column = 0)

		self.bfin = Tkinter.Button(self.elabel,font=("Helvetica", 10), text = "Final", command = self.press_fin)
		self.bfin.grid(row= 0, column = 1)

		self.labspace = Tkinter.Label(self,font=("Helvetica", 10), text = " ")
		self.labspace.grid(row = 2, column = 0)

		self.bpart = Tkinter.Button(self.mainframe,font=("Helvetica", 10), text = "Participation", command = self.press_part)
		self.bpart.grid(row= 3, column = 0)

		self.entryvarp = Tkinter.StringVar()
		self.entryvarp = Tkinter.Entry(self,font=("Helvetica", 10), textvariable = self.entryvarp)

		self.label = Tkinter.Label(self,font=("Helvetica", 10), text = "Enter Grade: ")

		self.button = Tkinter.Button(self,font=("Helvetica", 10), text = "Finished", command = self.enter_grade)


	def press_q1(self): 
		self.mainframe.grid_forget()
		self.entryvarp.grid(row = 0, column = 1)
		self.label.grid(row = 0, column = 0)
		self.button.grid(row = 1, column = 0, columnspan = 2)
		self.assess = 'q1'

	def press_q2(self): 
		self.mainframe.grid_forget()
		self.entryvarp.grid(row = 0, column = 1)
		self.label.grid(row = 0, column = 0)
		self.button.grid(row = 1, column = 0, columnspan = 2)
		self.assess = 'q2'

	def press_q3(self): 
		self.mainframe.grid_forget()
		self.entryvarp.grid(row = 0, column = 1)
		self.label.grid(row = 0, column = 0)
		self.button.grid(row = 1, column = 0, columnspan = 2)
		self.assess = 'q3'

	def press_q4(self): 
		self.mainframe.grid_forget()
		self.entryvarp.grid(row = 0, column = 1)
		self.label.grid(row = 0, column = 0)
		self.button.grid(row = 1, column = 0, columnspan = 2)
		self.assess = 'q4'

	def press_q5(self): 
		self.mainframe.grid_forget()
		self.entryvarp.grid(row = 0, column = 1)
		self.label.grid(row = 0, column = 0)
		self.button.grid(row = 1, column = 0, columnspan = 2)
		self.assess = 'q5'

	def press_q6(self): 
		self.mainframe.grid_forget()
		self.entryvarp.grid(row = 0, column = 1)
		self.label.grid(row = 0, column = 0)
		self.button.grid(row = 1, column = 0, columnspan = 2)
		self.assess = 'q6'

	def press_mid(self): 
		self.mainframe.grid_forget()
		self.entryvarp.grid(row = 0, column = 1)
		self.label.grid(row = 0, column = 0)
		self.button.grid(row = 1, column = 0, columnspan = 2)
		self.assess = 'mid'

	def press_fin(self): 
		self.mainframe.grid_forget()
		self.entryvarp.grid(row = 0, column = 1)
		self.label.grid(row = 0, column = 0)
		self.button.grid(row = 1, column = 0, columnspan = 2)
		self.assess = 'fin'

	def press_part(self): 
		self.mainframe.grid_forget()
		self.entryvarp.grid(row = 0, column = 1)
		self.label.grid(row = 0, column = 0)
		self.button.grid(row = 1, column = 0, columnspan = 2)
		self.assess = 'part'

	def enter_grade(self): 
		num = self.entryvarp.get()
		if self.assess == 'q1': 
			self.info.quiz_1 = int(num)
		elif self.assess == 'q2': 
			self.info.quiz_2 = int(num)
		elif self.assess == 'q3': 
			self.info.quiz_3 = int(num)
		elif self.assess == 'q4': 
			self.info.quiz_4 = int(num)
		elif self.assess == 'q5': 
			self.info.quiz_5 = int(num)
		elif self.assess == 'q6': 
			self.info.quiz_6 = int(num)
		elif self.assess == 'mid': 
			self.info.midterm = int(num)
		elif self.assess == 'fin': 
			self.info.final = int(num)
		elif self.assess == 'part': 
			self.info.participation = int(num)
		self.destroy()


# Add All Grades : Student Pane (This brings up a dialogue to add a grade for each student on an assignment)

class AddAllGrades(Tkinter.Toplevel):
	def __init__(self, parent, info):
		Tkinter.Toplevel.__init__(self, parent)
		self.info = info
		self.parent = parent
		self.initialize()

	def initialize(self):
		
		self.labelq1 = Tkinter.Label(self,font=("Helvetica", 10), text = "Quiz 1: ")
		self.labelq1.grid(row = 0, column = 0)

		self.labelq2 = Tkinter.Label(self,font=("Helvetica", 10), text = "Quiz 2: ")
		self.labelq2.grid(row = 1, column = 0)

		self.labelq3 = Tkinter.Label(self,font=("Helvetica", 10), text = "Quiz 3: ")
		self.labelq3.grid(row = 2, column = 0)

		self.labelq4 = Tkinter.Label(self,font=("Helvetica", 10), text = "Quiz 4: ")
		self.labelq4.grid(row = 3, column = 0)

		self.labelq5 = Tkinter.Label(self,font=("Helvetica", 10), text = "Quiz 5: ")
		self.labelq5.grid(row = 4, column = 0)

		self.labelq6 = Tkinter.Label(self,font=("Helvetica", 10), text = "Quiz 6: ")
		self.labelq6.grid(row = 5, column = 0)

		self.labelmid = Tkinter.Label(self,font=("Helvetica", 10), text = "Midterm: ")
		self.labelmid.grid(row = 6, column = 0)

		self.labelfin = Tkinter.Label(self,font=("Helvetica", 10), text = "Final: ")
		self.labelfin.grid(row = 7, column = 0)

		self.labelpart = Tkinter.Label(self,font=("Helvetica", 10), text = "Participation: ")
		self.labelpart.grid(row = 8, column = 0)

		self.entryvarq1 = Tkinter.StringVar()
		self.entryvarq1 = Tkinter.Entry(self,font=("Helvetica", 10), textvariable = self.entryvarq1)
		self.entryvarq1.grid(row = 0, column =1)

		self.entryvarq2 = Tkinter.StringVar()
		self.entryvarq2 = Tkinter.Entry(self,font=("Helvetica", 10), textvariable = self.entryvarq2)
		self.entryvarq2.grid(row = 1, column =1)

		self.entryvarq3 = Tkinter.StringVar()
		self.entryvarq3 = Tkinter.Entry(self,font=("Helvetica", 10), textvariable = self.entryvarq3)
		self.entryvarq3.grid(row = 2, column =1)

		self.entryvarq4 = Tkinter.StringVar()
		self.entryvarq4 = Tkinter.Entry(self,font=("Helvetica", 10), textvariable = self.entryvarq4)
		self.entryvarq4.grid(row = 3, column =1)

		self.entryvarq5 = Tkinter.StringVar()
		self.entryvarq5 = Tkinter.Entry(self,font=("Helvetica", 10), textvariable = self.entryvarq5)
		self.entryvarq5.grid(row = 4, column =1)

		self.entryvarq6 = Tkinter.StringVar()
		self.entryvarq6 = Tkinter.Entry(self,font=("Helvetica", 10), textvariable = self.entryvarq6)
		self.entryvarq6.grid(row = 5, column =1)

		self.entryvarmid = Tkinter.StringVar()
		self.entryvarmid = Tkinter.Entry(self,font=("Helvetica", 10), textvariable = self.entryvarmid)
		self.entryvarmid.grid(row = 6, column =1)

		self.entryvarfin = Tkinter.StringVar()
		self.entryvarfin = Tkinter.Entry(self,font=("Helvetica", 10), textvariable = self.entryvarfin)
		self.entryvarfin.grid(row = 7, column =1)

		self.entryvarpart = Tkinter.StringVar()
		self.entryvarpart = Tkinter.Entry(self,font=("Helvetica", 10), textvariable = self.entryvarpart)
		self.entryvarpart.grid(row = 8, column =1)

		self.donebutton = Tkinter.Button(self,font=("Helvetica", 10), text = 'Finished', command = self.donebut)
		self.donebutton.grid(row = 9, column = 0, columnspan = 2,sticky = 'w'+'e'+'n'+'s')

	def donebut(self):
		q1 = self.entryvarq1.get()
		iq1 = int(q1)
		self.info.quiz_1 = iq1

		q2 = self.entryvarq2.get()
		iq2 = int(q2)
		self.info.quiz_2 = iq2

		q3 = self.entryvarq3.get()
		iq3 = int(q3)
		self.info.quiz_3 = iq3

		q4 = self.entryvarq4.get()
		iq4 = int(q4)
		self.info.quiz_4 = iq4

		q5 = self.entryvarq5.get()
		iq5 = int(q5)
		self.info.quiz_5 = iq5

		q6 = self.entryvarq6.get()
		iq6 = int(q6)
		self.info.quiz_6 = iq6

		mid = self.entryvarmid.get()
		imid = int(mid)
		self.info.midterm = imid

		fin = self.entryvarfin.get()
		ifin = int(fin)
		self.info.final = ifin

		part = self.entryvarpart.get()
		ipart = int(part)
		self.info.participation = ipart

		self.destroy()

# FinishGrades : Student Pane (This adds all the missing grades for a student in the class)

class FinishGrade(Tkinter.Toplevel):
	def __init__(self, parent,info):
		Tkinter.Toplevel.__init__(self, parent)
		self.info = info
		self.parent = parent
		self.initialize()

	def initialize(self):

		
		self.lframe1 = Tkinter.LabelFrame(self,font=("Helvetica", 10), text = "Scores", padx = 5, pady = 5)
		self.lframe1.grid(row = 0, column = 0)

		self.button = Tkinter.Button(self,font=("Helvetica", 10), text = "Done", command = self.fingrade)
		self.button.grid(row = 1, column =0 )
		

		 
		self.labela1 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = "Quiz 1: ")
		self.labela1.grid(row=0, column =0)

		self.labelb1 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = "Quiz 2: ")
		self.labelb1.grid(row=1, column =0)

		self.labelc1 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = "Quiz 3: ")
		self.labelc1.grid(row=2, column =0)

		self.labeld1 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = "Quiz 4: ")
		self.labeld1.grid(row=3, column =0)

		self.labele1 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = "Quiz 5: ")
		self.labele1.grid(row=4, column =0)

		self.labelf1 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = "Quiz 6: ")
		self.labelf1.grid(row=5, column =0)

		self.labelg1 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = "Midterm Exam: ")
		self.labelg1.grid(row=6, column =0)

		self.labelh1 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = "Final Exam: ")
		self.labelh1.grid(row=7, column =0)

		self.labeli1 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = "Participation: ")
		self.labeli1.grid(row=8, column =0)

		

		self.q1check = True
		if self.info.quiz_1 == 'N/A':
			self.entryvar1 = Tkinter.StringVar()
			self.entryvar1 = Tkinter.Entry(self.lframe1,font=("Helvetica", 10), textvariable = self.entryvar1)
			self.entryvar1.grid(row = 0, column = 1)
			self.q1check = False
		else: 	
			self.labela2 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = self.info.quiz_1)
			self.labela2.grid(row=0, column =1)

		self.q2check = True
		if self.info.quiz_2 == 'N/A':
			self.entryvar2 = Tkinter.StringVar()
			self.entryvar2 = Tkinter.Entry(self.lframe1,font=("Helvetica", 10), textvariable = self.entryvar2)
			self.entryvar2.grid(row = 1, column = 1)
			self.q2check = False
		else: 	
			self.labelb2 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = self.info.quiz_2)
			self.labelb2.grid(row=1, column =1)

		
		self.q3check = True
		if self.info.quiz_3 == 'N/A':
			self.entryvar3 = Tkinter.StringVar()
			self.entryvar3 = Tkinter.Entry(self.lframe1,font=("Helvetica", 10), textvariable = self.entryvar3)
			self.entryvar3.grid(row = 2, column = 1)
			self.q3check = False
		else: 	
			self.labelb3 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = self.info.quiz_3)
			self.labelb3.grid(row=2, column =1)
		

		self.q4check = True
		if self.info.quiz_4 == 'N/A':
			self.entryvar4 = Tkinter.StringVar()
			self.entryvar4 = Tkinter.Entry(self.lframe1,font=("Helvetica", 10), textvariable = self.entryvar4)
			self.entryvar4.grid(row = 3, column = 1)
			self.q4check = False
		else: 	
			self.labelb3 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = self.info.quiz_4)
			self.labelb3.grid(row=3, column =1)

		self.q5check = True
		if self.info.quiz_5 == 'N/A':
			self.entryvar5 = Tkinter.StringVar()
			self.entryvar5 = Tkinter.Entry(self.lframe1,font=("Helvetica", 10), textvariable = self.entryvar5)
			self.entryvar5.grid(row = 4, column = 1)
			self.q5check = False
		else: 	
			self.labelb4 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = self.info.quiz_5)
			self.labelb4.grid(row=4, column =1)

		self.q6check = True
		if self.info.quiz_6 == 'N/A':
			self.entryvar6 = Tkinter.StringVar()
			self.entryvar6 = Tkinter.Entry(self.lframe1,font=("Helvetica", 10), textvariable = self.entryvar6)
			self.entryvar6.grid(row = 5, column = 1)
			self.q6check = False
		else: 	
			self.labelc2 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = self.info.quiz_6)
			self.labelc2.grid(row= 5, column =1)


		self.midcheck = True
		if self.info.midterm == 'N/A':
			self.entryvarm = Tkinter.StringVar()
			self.entryvarm = Tkinter.Entry(self.lframe1,font=("Helvetica", 10), textvariable = self.entryvarm)
			self.entryvarm.grid(row = 6, column = 1)
			self.midcheck = False
		else: 	
			self.labele2 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = self.info.midterm)
			self.labele2.grid(row=6, column =1)
		

		self.fincheck = True
		if self.info.final == 'N/A':
			self.entryvarf = Tkinter.StringVar()
			self.entryvarf = Tkinter.Entry(self.lframe1,font=("Helvetica", 10), textvariable = self.entryvarf)
			self.entryvarf.grid(row = 7, column = 1)
			self.fincheck = False
		else: 	
			self.labele3 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = self.info.final)
			self.labele3.grid(row=7, column =1)
		

		self.parcheck = True
		if self.info.participation == 'N/A':
			self.entryvarp = Tkinter.StringVar()
			self.entryvarp = Tkinter.Entry(self.lframe1,font=("Helvetica", 10), textvariable = self.entryvarp)
			self.entryvarp.grid(row = 8, column = 1)
			self.parcheck = False
		else: 	
			self.labele4 = Tkinter.Label(self.lframe1,font=("Helvetica", 10), text = self.info.participation)
			self.labele4.grid(row=8, column =1)
		
		
		
		

	def fingrade(self):
		err = False
		if not self.q1check: 
			c = self.entryvar1.get()
			if not c.isdigit(): 
				error = tkMessageBox.showinfo('Error', 'The grade must be a number')
				err = True
			else:  
				self.info.quiz_1 = int(c)

		if not self.q2check: 
			c = self.entryvar2.get()
			if not c.isdigit(): 
				error = tkMessageBox.showinfo('Error', 'The grade must be a number')
				err = True
			else:  
				self.info.quiz_2 = int(c)

		if not self.q3check: 
			c = self.entryvar3.get()
			if not c.isdigit(): 
				error = tkMessageBox.showinfo('Error', 'The grade must be a number')
				err = True
			else:  
				self.info.quiz_3 = int(c)

		if not self.q4check: 
			c = self.entryvar4.get()
			if not c.isdigit(): 
				error = tkMessageBox.showinfo('Error', 'The grade must be a number')
				err = True
			else:  
				self.info.quiz_4 = int(c)

		if not self.q5check: 
			c = self.entryvar5.get()
			if not c.isdigit(): 
				error = tkMessageBox.showinfo('Error', 'The grade must be a number')
				err = True
			else:  
				self.info.quiz_5 = int(c)

		if not self.q6check: 
			c = self.entryvar6.get()
			if not c.isdigit(): 
				error = tkMessageBox.showinfo('Error', 'The grade must be a number')
				err = True
			else:  
				self.info.quiz_6 = int(c)

		if not self.midcheck: 
			c = self.entryvarm.get()
			if not c.isdigit(): 
				error = tkMessageBox.showinfo('Error', 'The grade must be a number')
				err = True
			else:  
				self.info.midterm = int(c)

		if not self.fincheck: 
			c = self.entryvarf.get()
			if not c.isdigit(): 
				error = tkMessageBox.showinfo('Error', 'The grade must be a number')
				err = True
			else:  
				self.info.final = int(c)

		if not self.parcheck: 
			c = self.entryvarp.get()
			if not c.isdigit(): 
				error = tkMessageBox.showinfo('Error', 'The grade must be a number')
				err = True
			else:  
				self.info.participation = int(c)
		if not err:
			self.destroy()



#Load Class: This opens the class that has been loaded from the main app. 

class Load(Tkinter.Tk):
	def __init__(self, parent, info):
		Tkinter.Tk.__init__(self, parent)
		self.info = info
		self.parent = parent
		self.initialize()

	def initialize(self):
		a = self.info.replace(' ', '_')
		 
		self.grid()
		self.students = pickle.load(open( "save."+str(a), "rb" ))
		# Uncomment to print a list of students
		# for x in self.students:
		# 	print x.name
		self.label = Tkinter.Label(self, text = self.info, font = ("Helvetica", 10))
		self.label.grid(row = 0, column = 0)
		
		self.frame = Tkinter.LabelFrame(self,font=("Helvetica", 10),text = 'Roster', padx = 5, pady = 5)
		self.frame.grid(row = 1, column = 0,columnspan = 2)
		
		count = 0 
		ccount = 0
		for x in self.students:
			if count == 10: 
				ccount = ccount +1
				count = 0
			self.label = Tkinter.Label(self.frame,font=("Helvetica", 10), text = str(self.students.index(x)+1) +' '+ str(x.name), anchor = 'w')
			self.label.grid(row = count, column = ccount)
			count = count+1


		self.button1 = Tkinter.Button(self,font=("Helvetica", 10),text = "Student", command = self.open_student)
		self.button1.grid(row = 2, column = 0,sticky = 'w'+'e'+'n'+'s')

		self.button2 = Tkinter.Button(self,font=("Helvetica", 10), text = "Class", command = self.open_class)
		self.button2.grid(row = 2 , column =1,sticky = 'w'+'e'+'n'+'s')

		self.button3 = Tkinter.Button(self,font=("Helvetica", 10),text = "Add Student", command = self.new_student)
		self.button3.grid(row = 3, column = 0,sticky = 'w'+'e'+'n'+'s')

		self.button4 = Tkinter.Button(self,font=("Helvetica", 10), text = "Remove Student", command = self.remove_student)
		self.button4.grid(row = 3, column = 1, sticky = 'w'+'e'+'n'+'s')

		
		

	def open_student(self): 
		new_window = StudentPane(None, self.info)
		new_window.title("Students")

	def open_class(self):
		new_window = ClassPane(None, self.info)
		new_window.title("Class")

	def new_student(self): 
		new_window = NewStudent(None, self.info)
		new_window.title("Add a Student")

	def remove_student(self):
		new_window = RemoveStudent(None, self.info)
		new_window.title("Remove a Student")

#Remove a Student : Load Class

class RemoveStudent(Tkinter.Tk):
	def __init__(self, parent, info):
		Tkinter.Tk.__init__(self,parent)
		self.info = info
		self.parent = parent 
		self.initialize()

	def initialize(self):

		a = self.info.replace(' ', '_')
		self.students = pickle.load(open( "save."+str(a), "rb" ))

		self.frame = Tkinter.LabelFrame(self,font=("Helvetica", 10),text = 'Classes', padx = 5, pady = 5)
		self.frame.grid(row = 0, column  = 0)

		self.list = Tkinter.Listbox(self.frame,font=("Helvetica", 10))
		self.list.pack(side = 'left')
		content = []
		for x in self.students: 
			content.append(x.name)

		for x in content: 
			self.list.insert('end',str(x.strip()))

		self.button = Tkinter.Button(self,font=("Helvetica", 10), text = "Remove Student", command = self.remove)
		self.button.grid(row = 1, column = 0, sticky = 'w'+'e'+'n'+'s')


	def remove(self):
		if self.list.curselection() == (): 
			error = tkMessageBox.showinfo('Error', 'You must select a student.')

		else:
			a = self.info.replace(' ', '_')
			self.students = pickle.load(open( "save."+str(a), "rb" ))
			i = self.list.curselection()[0]
			t = self.list.get(i) 
			check =tkMessageBox.askquestion('Remove Student', 'Are you sure you want to remove '+ str(t)+' from the roster?', icon = 'warning')
			if check == 'yes':
				for x in self.students: 
					if x.name == t: 
						self.students.remove(x)
				pickle.dump(self.students, open( "save."+str(a), "wb" ) )
				self.destroy()
			else: 
				self.destroy()

			

		




# Add a New Student : Load Class

class NewStudent(Tkinter.Tk):
	def __init__(self, parent, info):
		Tkinter.Tk.__init__(self, parent)
		self.info = info
		self.parent = parent
		self.initialize()

	def initialize(self):
		self.a = self.info.replace(' ', '_')
		self.students = pickle.load(open( "save."+str(self.a), "rb" ))

		firstnamelabel = Tkinter.Label(self,font=("Helvetica", 10), text = "First Name")
		firstnamelabel.grid(row = 0, column = 0)

		self.entryvar1 = Tkinter.StringVar()
		self.entryvar1 = Tkinter.Entry(self, font=("Helvetica", 10),textvariable = self.entryvar1)
		self.entryvar1.grid(row = 0, column = 1)

		lastnamelabel = Tkinter.Label(self,font=("Helvetica", 10), text = "Last Name")
		lastnamelabel.grid(row = 1, column = 0)

		self.entryvar2 = Tkinter.StringVar()
		self.entryvar2 = Tkinter.Entry(self,font=("Helvetica", 10), textvariable = self.entryvar2)
		self.entryvar2.grid(row = 1, column = 1)

		button = Tkinter.Button(self,font=("Helvetica", 10), text = "Finished", command = self.finish)
		button.grid(row = 2, column = 0, columnspan = 2)

	def finish(self):
		if self.entryvar1 == '' or self.entryvar2 == '':
			error = tkMessageBox.showinfo('Error', 'You must fill in all fields.')
		
		else:
			fn = self.entryvar1.get()
			ln = self.entryvar2.get() 
			ns = Student(ln+", "+fn, 'N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A')
			self.students.append(ns)
			pickle.dump(self.students, open( "save."+str(self.a), "wb" ) )
			self.destroy()



# Window to add a class

class AddAClass(Tkinter.Toplevel):
	def __init__(self,parent):
		Tkinter.Toplevel.__init__(self,parent) 
		self.parent  = parent
		self.initialize()

	def initialize(self):
		# Create a container

		self.classname = '' 
		self.classsize = 0

		self.frame = Tkinter.Frame(self)
		self.frame.pack()

		self.label1 = Tkinter.Label(self.frame,font=("Helvetica", 10), text = "Class Name: ")
		self.label1.grid(row = 0, column = 0)

		self.entryvar1 = Tkinter.StringVar()
		self.entryvar1 = Tkinter.Entry(self.frame,font=("Helvetica", 10), textvariable = self.entryvar1)
		self.entryvar1.grid(row = 0, column = 1)

		self.label2 = Tkinter.Label(self.frame,font=("Helvetica", 10), text = "Number of Students: ")
		self.label2.grid(row = 1, column = 0)

		self.entryvar2 = Tkinter.StringVar()
		self.entryvar2 = Tkinter.Entry(self.frame,font=("Helvetica", 10), textvariable = self.entryvar2)
		self.entryvar2.grid(row = 1, column = 1)

		self.button = Tkinter.Button(self.frame,font=("Helvetica", 10), text = 'Add Students', command = self.add_students)
		self.button.grid(row =2, column =0, columnspan = 2,sticky = 'w'+'e'+'n'+'s')

	def add_students(self):
		a = self.entryvar1.get()
		b = a.replace(' ', '_')
		self.classname = b
		 

		c = self.entryvar2.get()
		if not c.isdigit(): 
			error = tkMessageBox.showinfo('Error', 'The number of students must be a number')
		else: 
			self.classsize = int(c)
			for x in range(self.classsize):
				toplevel = AddStudents(None)

			self.frame.destroy()
			self.button2 = Tkinter.Button(self,text = 'Finish',font=("Helvetica", 10), command = self.finish)
			self.button2.pack()
	
	def finish(self):
		pickle.dump( students, open( "save."+str(self.classname), "wb" ) )
		f = open("Classes", "r")
		R = f.readlines()
		f.close()

		c = self.classname.replace('_', ' ')
		R.append(c + '\n')
		
		g = open('Classes', "w")
		for x in R: 
			g.write(x)
		g.close()

		self.destroy()

#Window for adding student names : AddAClass. 

class AddStudents(Tkinter.Toplevel):
	def __init__(self,parent):
		Tkinter.Toplevel.__init__(self,parent) 
		self.parent  = parent
		self.initialize()

	def initialize(self):

		self.label3 = Tkinter.Label(self,font=("Helvetica", 10), text = 'Enter student names')
		self.label3.pack()

		self.frame = Tkinter.Frame(self)
		self.frame.pack()
			
		
		self.labeln1 = Tkinter.Label(self.frame,font=("Helvetica", 10), text = "First Name: ")
		self.labeln1.grid(row = 0, column = 0)
				
		self.entryvarn1 = Tkinter.StringVar()
		self.entryvarn1 = Tkinter.Entry(self.frame,font=("Helvetica", 10), textvariable = self.entryvarn1)
		self.entryvarn1.grid(row = 0, column = 1)

		self.labeln12 = Tkinter.Label(self.frame,font=("Helvetica", 10), text = "Last Name: ")
		self.labeln12.grid(row = 1, column = 0)
				
		self.entryvarn2 = Tkinter.StringVar()
		self.entryvarn2 = Tkinter.Entry(self.frame,font=("Helvetica", 10), textvariable = self.entryvarn2)
		self.entryvarn2.grid(row = 1, column = 1)

		self.button = Tkinter.Button(self.frame, text = "Add Student",font=("Helvetica", 10), command = self.add_student)
		self.button.grid(row = 2, column = 0, columnspan = 2,sticky = 'w'+'e'+'n'+'s')

	def add_student(self):
		global students

		first = self.entryvarn1.get()
		second = self.entryvarn2.get()
		name = second+', '+first 
		 
		st = Student(name, 'N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A')
		students.append(st)
		self.destroy()

# Main App

class App(Tkinter.Tk): 
	def __init__(self,parent):
		Tkinter.Tk.__init__(self,parent)
		self.parent = parent
		self.initialize()

	def initialize(self):
		self.grid()

		# menubar = Tkinter.MenuBar(self)
		# self.config(menu= menubar)
		f = open('Classes','r')
		content = f.readlines()
		f.close()

		self.til = Tkinter.Label(self, text = "Select a Class",font=("Helvetica", 10))
		self.til.grid(row = 0, column = 0, columnspan = 2)

		self.frame = Tkinter.LabelFrame(self,text = 'Classes', padx = 5, pady = 5,font=("Helvetica", 10))
		self.frame.grid(row = 1, column = 0, columnspan = 2)
		self.list = Tkinter.Listbox(self.frame,font=("Helvetica", 10))
		self.list.pack(side = 'left')
		self.list.config(width=30)
		for x in content: 
			self.list.insert('end',str(x.strip()))

		self.loadbutton = Tkinter.Button(self, text = 'Load',font=("Helvetica", 10), command = self.load_class )
		self.loadbutton.grid(row =2,column = 1,sticky = 'w'+'e'+'n'+'s')

		self.addclassbutton = Tkinter.Button(self, text = "Add New Class", font=("Helvetica", 10), command = self.add_class)
		self.addclassbutton.grid(row = 3, column = 0, columnspan = 2,sticky = 'w'+'e'+'n'+'s')

		self.refreshlistbutton = Tkinter.Button(self, text = "Refresh",font=("Helvetica", 10), command = self.refresh)
		self.refreshlistbutton.grid(row = 2, column = 0,sticky = 'w'+'e'+'n'+'s')

	def load_class(self):
		if self.list.curselection() == (): 
			error = tkMessageBox.showinfo('Error', 'You must select a class')

		else: 
			i = self.list.curselection()[0]
			t = self.list.get(i)
			new_window = Load(None, t)
			new_window.title(t)
			self.destroy()

	def add_class(self): 
		toplevel = AddAClass(None)
		toplevel.title('Add a Class')

	def refresh(self): 
		self.list.delete(0, 'end')
		f = open('Classes','r')
		content = f.readlines()
		f.close()
		for x in content: 
			self.list.insert('end',str(x.strip()))

		


		

if __name__ == '__main__':
	
	app = App(None)
	app.title('Grade Application')
	

		
	
		

	


	app.mainloop()
