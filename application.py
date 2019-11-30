import os

from flask import Flask
from flask import render_template
from flask import request, redirect
import copy
import genetic_algo

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "database.db"))


app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Subject(db.Model):
    #id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(30), unique = True, nullable = False, primary_key = True)
    frequency = db.Column(db.String(2), nullable = False)

class Lecture(db.Model):
    subject_name = db.Column(db.String(30), unique = True, nullable = False, primary_key = True)
    class_name = db.Column(db.String(30), nullable = False)

class Teacher(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	teacher_name = db.Column(db.String(30),nullable = False)
	subject_name = db.Column(db.String(30),nullable = False)


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/subjects", methods=("GET","POST"))
def subjects():
    if request.method == "POST":
        subject = Subject(name=request.form.get("name"), frequency=request.form.get("frequency_"))
        db.session.add(subject)
        db.session.commit()

    subjects = Subject.query.all()

    return render_template("subjects.html", subjects=subjects)


@app.route("/update", methods=["POST"])
def sub_update():
    newname = request.form.get("newname")
    oldname = request.form.get("oldname")
    newfreq = request.form.get("newfreq")
    subject = Subject.query.filter_by(name=oldname).first()
    subject.name = newname
    subject.frequency = newfreq
    db.session.commit()
    return redirect("/subjects")


@app.route("/delete", methods=["POST"])
def sub_delete():
    name = request.form.get("name")
    subject = Subject.query.filter_by(name=name).first()
    db.session.delete(subject)
    db.session.commit()
    return redirect("/subjects")


@app.route("/teachers",methods=["GET","POST"])
def teachers():
	if request.method == "POST":
	    teacher_name = request.form.get("teacher_name")
	    subject_name = request.form.get("subject_code")
	    teacher = Teacher(teacher_name = teacher_name, subject_name = subject_name)
	    db.session.add(teacher)
	    db.session.commit()
	subject_names = Subject.query.all()
	teachers = Teacher.query.all()
	global teacher_names
	teacher_names = []
	for teacher in teachers:
		try:
			count = 0
			for i in teacher_names:
				if i[0]==teacher.teacher_name:
					i[1].append(teacher.subject_name)
					count = 1
					break
			if count == 0:
				teacher_names.append([teacher.teacher_name,[teacher.subject_name]])
		except:
				teacher_names.append([teacher.teacher_name,[teacher.subject_name]])

	return render_template("teachers.html", teacher_names=teacher_names,subject_names=subject_names, teachers= teachers)

@app.route("/delete_teacher", methods=["POST"])
def sub_delete_teacher():
    teacher_name = request.form.get("teacher_name")
    teacher = Teacher.query.filter_by(teacher_name=teacher_name).first()
    db.session.delete(teacher)
    db.session.commit()
    return redirect("/teachers")


@app.route("/classes", methods=("GET","POST"))
def classes():
	if request.method == "POST":
		lecture = Lecture(subject_name=request.form.get("subject_name"), class_name=request.form.get("class_name"))
		db.session.add(lecture)
		db.session.commit()
	global class_names
	class_names = {}
	lectures = Lecture.query.all()
	for lecture in lectures:
		try:
			class_names[lecture.class_name].append(lecture.subject_name)
		except:
			class_names[lecture.class_name] = []
			class_names[lecture.class_name].append(lecture.subject_name)
	return render_template("classes.html", lectures = lectures)


@app.route("/delete_lecture", methods=["POST"])
def sub_delete_lecture():
    subject_name = request.form.get("subject_name")
    lecture = Lecture.query.filter_by(subject_name=subject_name).first()
    db.session.delete(lecture)
    db.session.commit()
    return redirect("/classes")


slot_times=[]
options=[]

@app.route("/slots",methods=["GET","POST"])
def slots():
    if request.method == "POST":
        slot = request.form.get("slot")
        slot_times.append(slot)
        option=request.form["type"]
        options.append(option)
    l=len(slot_times)
    return render_template("timeslots.html",slot_times=slot_times,l=l,options=options)

days = ["Mon","Tues","Wed","Thurs","Fri"]


classes_={}

def class_type():
    time_slots = slot_times[:]
    temp_options = options[:]
    leng = len(slot_times)
    for i in range(leng):
        if options[i] == "Break":
            time_slots.remove(slot_times[i])
            temp_options.remove(options[i])
    return time_slots



def create_timetable():
	time_slots = class_type()
	for class_no in class_names.keys():
   	    classes_[class_no] = []
   	    for sub in class_names[class_no]:
   	        temp = []
   	        temp.append(sub)
           	subjects = Subject.query.all()
           	print(subjects)
           	for subject in subjects:
           	    if sub == subject.name:
           	        temp.append(int(subject.frequency))
           	for i in teacher_names:
           	    if sub in i[1]:
           	        temp.append(i[0])
           	classes_[class_no].append(temp)
	temp2_classes = copy.deepcopy(classes_)

	s = genetic_algo.Schedule(time_slots, days, temp2_classes)
	while (s.fitness != 1):
		temp2_classes = copy.deepcopy(classes_)
		s = genetic_algo.Schedule(time_slots, days, temp2_classes)
	print(s.timetable["Mon"])
	print(s.timetable["Tues"])
	print(s.timetable["Wed"])
	print(s.timetable["Thurs"])
	print(s.timetable["Fri"])
	print(s.fitness)
	return s


@app.route("/select",methods=["GET"])
def select():
    global s
    s=create_timetable()
    return render_template("open.html",class_names=class_names,teacher_names=teacher_names)


@app.route("/open/<string:class_name>")
def open(class_name):
    time_slots = class_type()
    return render_template("table.html", slot_times=slot_times,s=s,time_slots=time_slots,class_name=class_name)


@app.route("/opent/<string:teacher_name>")
def opent(teacher_name):
    time_slots = class_type()
    return render_template("teacher_table.html", slot_times=slot_times,s=s,time_slots=time_slots,teacher_name=teacher_name)

@app.route("/help")
def help():
    return render_template("help.html")

if __name__ == "__main__":
    app.run(debug=True)







