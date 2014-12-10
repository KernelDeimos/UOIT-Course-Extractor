#!/usr/bin/python
# can't use Python3 due to incompabtibility with BS4

import urllib, urllib2 # library for fetching webpages
from bs4 import BeautifulSoup # library for parsing webpages
import sqlite3

import time

"""
Tutorials used in this project:

https://docs.python.org/2/howto/urllib2.html
http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser

TODO:
 - Try out that Go thing
"""

"""
http://uoit.ca/mycampus/avail_courses.html

Information gathered from checking out the webpage
--------------------------------------------------
Helpful Pages:
http://www.uoit.ca/main/current-students/academics-and-programs/academic-calendars/

Start on:
/prod/bwckschd.p_disp_dyn_sched?TRM=U

===THE COURSES PAGE===
POST /prod/bwckgens.p_proc_term_date -> the courses page
p_calling_proc = bwckschd.p_disp_dyn_sched
TRM = U
p_term = 201501 # that's for 2015 JAN term

No generated # or anything... so hopefully it doesn't land on the "break-in" page :/



===COURSE NUMBERS===
First digit is from 1-4
Second and thrid digits basically anything
Fourth most probably 1, 0, likely <=5
GO WITH SMALLER #s FIRST!!

Okay... I guess the easiest way to do this is to add all the courses manually
The systematic approach might be okay if i make sure I don't send too many requests too quickly.



===SEARCH SUBMISSION===
POST /prod/bwckschd.p_get_crse_unsec
Try without the dummy vals
term_in = 201501
sel_subj = MATH
sel_crse = 1010
sel_title = ""
sel_schd = %
sel_insm = %
sel_from_cred = ""
sel_to_cred = ""
sel_camp="%"
begin_hh = ""
begin_mi = ""
begin_ap = ""
end_hh = ""
end_mi = ""
end_ap = ""
sel_day = "dummy"

sel_levl = "dummy"
sel_sess = "dummy"
sel_instr = "dummy"
sel_ptrm = "dummy"
sel_attr = "dummy"

I tihnk that's all of them! :D

... and that was when I realized I can just look at the headers my browser sends ...

"""

"""
class UOITCourseFetcher:
	def __init__(self,info):
		self.info = inf
	def load_
"""

class PostData:
	def __init__(self):
		self.items = []
	def add_item(self,name,value):
		self.items.append([name,value])
	def get_string(self):
		# Python for the win! Love one-lining this stuff!
		res = '&'.join([item[0] + "=" + item[1] for item in self.items])
		print(res)
		return res

class CourseClassTime:
	def __init__(self,week,startTime,endTime,startDate,endDate,day,room,ctype,profs):
		# It's *almost* at the point where I shoud've just used a dictionary
		# This will be better if I need to treat certain values differently though.
		self.week = week
		self.startTime = startTime
		self.endTime = endTime
		self.startDate = startDate
		self.endDate = endDate
		self.day = day
		self.room = room
		self.ctype = ctype
		self.profs = profs
	def get_type(self):
		return self.ctype
	def get_info(self):
		return {
			'week':self.week,
			'stime':self.startTime,
			'etime':self.endTime,
			'sdate':self.startDate,
			'edate':self.endDate,
			'day':self.day,
			'room':self.room,
			'type':self.ctype,
			'profs':self.profs
			}
	def __str__(self):
		ret = ""
		ret = "---   Time     ---\n"
		ret += "Week: \t" + str(self.week) + "\n"
		ret += "Day: \t" + str(self.day) + "\n"
		ret += "Start: \t" + self.startTime.strftime("%I:%M %p") + "\n"
		ret += "End: \t" + self.endTime.strftime("%I:%M %p") #+ "\n"
		#ret += "------------------ [end class info]"
		return ret

class CourseClass:
	""" Will hold all information about a particular CRN """
	def __init__(self,crn,course,sec):
		""" Course class: contains CRN info and dates/times list """
		self.crn = int(crn)
		self.course = course # ptr to a Course obj
		self.sec = sec

		self.classTimes = []
	def set_prop(self,key,val):
		self.info[key] = val
	def get_info(self):
		return self.crn, self.course.get_ccode()
	def get_times(self):
		return self.classTimes
	def add_time(self,classTime):
		self.classTimes.append(classTime)
	def __str__(self):
		ret = ""
		ret = "---   Class    ---\n"
		ret += "CRN: \t\t" + str(self.crn) + "\n"
		ret += "Sections: \t" + str(len(self.classTimes)) + "\n"
		ret += "Types: \t" + ', '.join([sec.get_type() for sec in self.classTimes]) + "\n"

		#ret += "------------------ [end class info]"
		return ret

class Course:
	# MAKING THIS WAS A WASTE OF TIME
	# BUT IT MAKES THE CODE COOLER
	def __init__(self,ccode,name):
		self.ccode = ccode
		self.name = name
		# set subject (MATH), course number (1010U)
		self.subj, self.courseNoX = self.ccode.split(' ') # ['MATH', '1010U']
		# 4-character course code (1010)
		self.courseNo4 = self.courseNoX[0:4]
	def get_ccode(self):
		return self.ccode
	def get_info(self):
		return self.name, self.subj, self.courseNo4, self.courseNoX
	def check_ccode(self,ccode):
		return ccode == self.ccode
	def __str__(self):
		ret = ""
		ret = "===   Course   ===\n"
		ret += self.ccode + " - " + self.name + "\n"
		#ret += "------------------ [end course info]"
		return ret

class CourseError(Exception):
	pass
class CourseDataMgr:
	def __init__(self):
		self.courses = []
		self.classes = []
	def find_course(self,ccode):
		for c in self.courses:
			if c.check_ccode(ccode):
				return c
		raise CourseError
	def check_course_exists(self,ccode):
		for c in self.courses:
			if c.check_ccode(ccode):
				return true
		return false
	def add_course(self,cobj):
		self.courses.append(cobj)
	def add_class(self,cobj):
		self.classes.append(cobj)
	def print_count(self):
		print("Courses: " + str(len(self.courses)))
		print("Classes: " + str(len(self.classes)))


class CourseExtractor:
	def __init__(self,info,logFileHandler,cdm):
		self.info = info
		self.logfh = logFileHandler
		self.cdm = cdm # course data manager
		# Quick Test...
		"""
		url = info['url_base'] + info['url_searchpage']
		vals = {'p_calling_proc' : "bwckschd.p_disp_dyn_sched",
				'TRM' : "U",
				'p_term' : "201501"}
		data = urllib.urlencode(vals)
		req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)
		print(response.read())
		"""
	def god_damnit_split(self,txt):
		txt = txt.split(' - ')
		howMany = 0
		while True:
			try:
				int(txt[howMany])
				break
			except ValueError:
				pass # FUCK
			howMany += 1
		v1 = ' - '.join(txt[0:howMany])
		v2 = txt[howMany+0]
		v3 = txt[howMany+1]
		v4 = txt[howMany+2]
		return [v1,v2,v3,v4]

	def run(self,subj):
		# Obtain HTML
		res = self.get_course_results(subj)
		#res = self.get_test_html("test.html")

		# Log information for future reference
		self.log_time()
		self.logfh.write(res)

		# Generate BeautifulSoup object
		doThing = 0 # for testing
		soup = BeautifulSoup(res)

		# Initialize some things before extracting
		cdm = self.cdm

		courseObj = None
		classObj = None

		TESTVAL_times = 0
		TESTVAL_cours = 0

		# EXTRACT THE INFO!!
		for table in soup.find_all('table'):
			for tElem in table.children:
				# Header for a new class
				if tElem.name == "th": # Will always be header for a new class
					# Split up class info, set variables
					classinfo = self.god_damnit_split(tElem.get_text())

					i_ctitle 	=     classinfo[0] # like, the title of the course.
					i_crn 		= int(classinfo[1])
					i_ccode 	=     classinfo[2]
					i_section 	=     classinfo[3]

					try:
						courseObj = cdm.find_course(i_ccode)
					except CourseError:
						TESTVAL_cours += 1
						courseObj = Course(i_ccode,i_ctitle)
						cdm.add_course(courseObj)

					classObj = CourseClass(i_crn,courseObj,i_section)
					cdm.add_class(classObj)
					# Confirmed that these are all ddheader items
					# Each thing here will contain information for a particular CRN!
				if tElem.name == "tr": # table rows in main table
					for td in tElem.children: # table cells in main table
						if td.name == "td": # only parse if it's a table cell
							for thing in td.children: # go through everything in the cell

								# ANYTHING IN A TABLE CELL OF THE MAIN TABLE
								if thing.name == "table": # any table within a cell
									if thing.caption.get_text() == "Scheduled Meeting Times":
										# If we're here, we're parsing a schedule table! Yay!
										TESTVAL_times += 1
										for row in thing.children:
											if row.name == "tr": # row containing a class time
												rowItems = []
												for item in row.children:
													if item.name == "td":
														rowItems.append(item)
												# pick out information about this class time
												week 	= rowItems[0].get_text()
												times 	= rowItems[2].get_text()
												day 	= rowItems[3].get_text()
												room 	= rowItems[4].get_text()
												dates 	= rowItems[5].get_text()
												ctype 	= rowItems[6].get_text()
												profs 	= rowItems[7].get_text()
												# Interesting question I pondered: why not just store the list as is?
												# Organization was my answer. It makes everything easier in the long-run.

												# Make sure this is an actual contents row
												if week == "Week" or times == "Time":
													# This means this is just the row of headings
													continue # Go to next iteration
												#print(type(times))
												if (times == "TBA"):
													#print("Time is TBA: Setting start & end to None")
													startTime = None
													endTime = None
												else:
													#print(times.split(' - '))
													startTime, endTime = times.split(' - ')
													startTime = time.strptime(startTime, "%I:%M %p")
													endTime = time.strptime(endTime, "%I:%M %p")

												if (dates == "TBA"):
													#print("Time is TBA: Setting start & end to None")
													startDate = None
													endDate = None
												else:
													#print(times.split(' - '))
													startDate, endDate = dates.split(' - ')
													startDate = time.strptime(startDate, "%b %d, %Y")
													endDate = time.strptime(endDate, "%b %d, %Y")

												classTime = CourseClassTime(
													week,startTime,endTime,startDate,
													endDate,day,room,ctype,profs
													)
												classObj.add_time(classTime)
		print("[DONE] Finished extracting from <TEST PARSE>")
		cdm.print_count()
		print("Check values: " + ', '.join([str(TESTVAL_times), str(TESTVAL_cours)])) # If this matches, this is good!


		return
		# SHOW SOME RESULTS! (temporary)
		for course in cdm.courses:
			print(course)
			for cla in cdm.classes:
				if cla.course.get_ccode() == course.get_ccode():
					print(cla)
					pass
			#print("=== End Course ===")



	def log_time(self):
		thing = "<!--TEST RUN ===\n"
		thing += time.strftime("%b %d, %I:%M %p")
		thing += "\n---------------->\n"
		self.logfh.write(thing)
	def get_test_html(self,filen):
		retVal = ""
		with open(filen, 'r') as f:
			retVal = f.read()
		return retVal

	def get_course_results(self,subj,cnum=""):
		""" Takes (subj,cnum) as STRINGS! """
		info = self.info # take info from self

		url = info['url_base'] + info['url_action']
		vals = PostData()
		vals.add_item('TRM'				, "U")
		vals.add_item('term_in'			, "201501")
		vals.add_item('sel_subj'		, "dummy")
		vals.add_item('sel_day'			, "dummy")
		vals.add_item('sel_schd'		, "dummy")
		vals.add_item('sel_insm'		, "dummy")
		vals.add_item('sel_camp'		, "dummy")
		vals.add_item('sel_levl'		, "dummy")
		vals.add_item('sel_sess'		, "dummy")
		vals.add_item('sel_instr'		, "dummy")
		vals.add_item('sel_ptrm'		, "dummy")
		vals.add_item('sel_attr'		, "dummy")
		vals.add_item('sel_subj'		, subj)
		vals.add_item('sel_crse'		, cnum)
		vals.add_item('sel_title'		, "")
		vals.add_item('sel_schd'		, "%")
		vals.add_item('sel_insm'		, "%")
		vals.add_item('sel_from_cred'	, "")
		vals.add_item('sel_to_cred'		, "")
		vals.add_item('sel_camp'		, "%")
		vals.add_item('begin_hh'		, "0")
		vals.add_item('begin_mi'		, "0")
		vals.add_item('begin_ap'		, "a")
		vals.add_item('end_hh'			, "0")
		vals.add_item('end_mi'			, "0")
		vals.add_item('end_ap'			, "a")

		#data = urllib.urlencode(vals.get_string())
		data = vals.get_string()
		req = urllib2.Request(url, data=data)
		print("=== Headers ===")
		print(req.headers)
		print("=== Data ===")
		print(req.data)
		response = urllib2.urlopen(req)
		return response.read()

class CourseStorer_SQLite:
	def __init__(self,cdm,inFile):
		self.cdm = cdm
		self.file = inFile
		self.conn = sqlite3.connect(inFile)

		c = self.conn.cursor()
		c.execute('''CREATE TABLE courses (
			ccode TEXT PRIMARY KEY,
			fname TEXT,
			subj TEXT,
			num INTEGER
			)''')
		c.execute('''CREATE TABLE classes (
			crn INTEGER PRIMARY KEY,
			course TEXT, -- maps to courses.ccode

			FOREIGN KEY(course) REFERENCES courses(ccode)
			)''')
		c.execute('''CREATE TABLE times (
			id INTEGER PRIMARY KEY, -- SQLite will autoinc
			crn INTEGER,

			-- date and time info
			stime TEXT,
			etime TEXT,
			sdate TEXT,
			edate TEXT,

			week TEXT, -- one or two
			day TEXT,

			-- other info
			room TEXT,
			type TEXT, -- Lecture, Lab, etc...
			profs TEXT,

			FOREIGN KEY(crn) REFERENCES classes(crn)
			)''')
		self.conn.commit()
	def run(self):
		cdm = self.cdm
		c = self.conn.cursor()
		for course in cdm.courses:
			sql = '''INSERT INTO courses(ccode,fname,subj,num)
				VALUES (?,?,?,?)'''
			ccode = course.get_ccode()
			info = course.get_info()
			c.execute(sql, (ccode,info[0],info[1],info[2]))

		for cla in cdm.classes:
			sql = '''INSERT INTO classes(crn,course)
				VALUES (?,?)'''
			info = cla.get_info() # crn, course
			crn = info[0]
			c.execute(sql, (crn, info[1]))
			for cTime in cla.get_times():
				sql = '''INSERT INTO times(crn,stime,etime,sdate,edate,week,day,room,type,profs)
				VALUES (?,?,?,?,?,?,?,?,?,?)'''
				cTimeInfo = cTime.get_info()

				startTime, endTime, startDate, endDate = "N/A", "N/A", "N/A", "N/A"
				try:
					startTime = time.strftime("%H:%M:%S", cTimeInfo['stime'])
					endTime = time.strftime("%H:%M:%S", cTimeInfo['etime'])
				except TypeError:
					startTime, endTime = "N/A", "N/A"
				try:
					startDate = time.strftime("%Y-%m-%d", cTimeInfo['sdate'])
					endDate = time.strftime("%Y-%m-%d", cTimeInfo['edate'])
				except TypeError:
					startDate, endDate = "N/A", "N/A"
					pass # values already set to N/A
				values = (
					crn,
					startTime,
					endTime,
					startDate,
					endDate,
					cTimeInfo['week'],
					cTimeInfo['day'],
					cTimeInfo['room'],
					cTimeInfo['type'],
					cTimeInfo['profs']
					)
				c.execute(sql,values)

		self.conn.commit()



def main():
	print("UOIT Course Data Extractor")
	print("written by KernelDeimos\n")
	info = {}
	info['url_base'] = "http://ssbp.mycampus.ca"
	info['url_landing'] = "/prod/bwckschd.p_disp_dyn_sched?TRM=U"
	info['url_searchpage'] = "/prod/bwckgens.p_proc_term_date"
	info['url_action'] = "/prod/bwckschd.p_get_crse_unsec"

	f = open('./logfile','w') # Change to append later!!
	f2 = "./courses.db"

	cdm = CourseDataMgr()
	ins = CourseExtractor(info,f,cdm)
	# Maybe later I'll make it fetch the subject names,
	# but for now this is just easier.
	
	for subj in [
		"ALSU","AEDT","ANTH","APBS","AUTE","BIOL","BUSI","CANN",
		"CHEM","CHIN","COMM","CDPS","CSCI","ECON","EDUC","ELEE",
		"ENGR","ENGL","ENVS","FSCI","FREN","GRMN","HLSC","HSST",
		"HIST","INFR","LGLS","MANE","MITS","MTSC","MATH","MECE",
		"MLSC","MCSC","NUCL","NURS","PHIL","PHY","POSC","PSYC",
		"RADI","SCCO","SSCI","SOCI","SOFE","STAT"
		]:
		print("==== SUBJECT PAGE: "+subj)
		ins.run(subj)
	

	"""
	for subj in ["ALSU","AEDT","ANTH"]:
		ins.run(subj)
	"""
	#ins.run("MATH")
	s1 = CourseStorer_SQLite(cdm, f2)
	s1.run()



if __name__ == "__main__":
	main()
