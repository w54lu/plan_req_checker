from uwaterlooapi import UWaterlooAPI


uw = UWaterlooAPI(api_key='a2c039eecf54ae35051d7d9072c102db')


def term_course_schedule (term, subject, catalog):
	schedule = uw.term_course_schedule(term, subject, catalog)
	return schedule


def schedule_by_class_numbers (class_numbers):
	result = []
	for class_number in class_numbers:
		schedule = uw.schedule_by_class_number(class_number)
		result.extend(schedule)

	return result


def schedule_by_class_number (class_number):
	schedule = uw.schedule_by_class_number(class_number)
	return schedule


def course_list (term, subject):
	result = []
	courses_by_term = uw.term_courses (term)
	course_by_subject = []
	for course in courses_by_term:
		if course.get ('subject') == subject:
			course_by_subject.append (course)

	for course in course_by_subject:
		course_detail = (uw.course (subject, course.get ('catalog_number')))
		result.append (course_detail)

	return result