# gradeapp
A gradebook program written using python and tkinter. 

# Installation
To install the program save grade.py and Classes in its own directory. It writes files for your classes to this directory. The file Classes keeps a list of the classes in the gradebook. Run the app by moving to the newly created directory in the terminal with 

cd PATH/TO/NEWDIR

and running the  python script with 

python grade.py

# Using the Gradebook

The gradebook opens first pane for managing the classes in the gradebook.

# Adding a New Class

To add a new class click the Add class button. This will open a new pane that asks for the name of the new class and the number of students in the class. This will prompt the user for the first and last name of each student in the class. 

# Loading a Class

Once a class has been created hitting the refresh button on the opening pane will reload the name of the classes. To load a class select it in the listbox and hit load. 

# The Class Pane 
Once a class has been loaded the add and remove students buttons allow you to edit the roster for the loaded class. The student and class panes are detailed below. 

# The Student Pane

The student pane is for doing actions with individual students. From there one can display a student's grade, calculate what their grade will be given other grades, add a single grade, add all their grades at once, or add any grades that have not yet been entered. These are accomplished by selecting the student to edit and clicking Display Grades, Calculate Grade, Add One Grade, Add All Grades, and Finish Grades respectively. 

# The Class Pane

The class pane is for doing actions with the entire class. Display Grades opens a new window to view the class averages for each particular assignment. Add Class Grades opens a pane to add a grade for every student for particular assignment. The Finalize Class button prompts the user for the remaining grades of every student. 

# Disadvantages

The major disavantage of this gradebook is that customizing it to your own class requires some knowledge of python. The gradebook as it is set up is used for my particular style of grading. In time I hope to make the gradebook modular in this respect. 
