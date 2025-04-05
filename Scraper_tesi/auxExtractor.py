# from constantsScraper import *

# # Class representing a course (Insegnamento)
# class Insegnamento:

#     def __init__(self, periodo, codice, nome: str, correlazione, crediti):
#         """
#         Initializes an Insegnamento (course) object.

#         Parameters:
#         - periodo: The academic period (semester or year).
#         - codice: Unique identifier code for the course.
#         - nome: The name of the course.
#         - correlazione: Correlation value for course relationships.
#         - crediti: The number of credits assigned to the course.
#         """
#         self.periodo = periodo
#         self.codice = codice
#         self.nome = nome
#         self.correlazione = correlazione
#         self.crediti = float(crediti)  # Convert credits to float for numerical operations
    
#     def __str__(self):
#         """Returns a string representation of the course object."""
#         return f"Insegnamento: {self.nome}, Codice: {self.codice}"
    
#     def __eq__(self, other):
#         """Checks equality based on the course code."""
#         return self.codice == other.codice
    
#     def __le__(self, other):
#         """Checks if one course code is less than or equal to another."""
#         return self.codice <= other.codice
    
#     def __lt__(self, other):
#         """Checks if one course code is less than another."""
#         return self.codice < other.codice
    
#     def __ge__(self, other):
#         """Checks if one course code is greater than or equal to another."""
#         return self.codice >= other.codice
    
#     def __gt__(self, other):
#         """Checks if one course code is greater than another."""
#         return self.codice > other.codice
    
#     def __hash__(self):
#         """Returns a hash based on the course code, making it usable in sets and dictionaries."""
#         return hash(self.codice)


# # Class representing a table (Tabella) that groups multiple courses
# class Tabella:
    
#     def __init__(self, nome: str, anno, crediti):
#         """
#         Initializes a Tabella (table) object.

#         Parameters:
#         - nome: The name of the table (category or group of courses).
#         - anno: The academic year associated with this table.
#         - crediti: The total number of credits available in this table.
#         """
#         self.nome = nome
#         self.anno = anno
#         self.crediti = float(crediti)  # Convert credits to float for numerical operations
#         self._lista_insegnamenti: list[Insegnamento] = []  # List of courses within this table


#     def get_lista_insegnamenti(self) -> list[Insegnamento]:
#         """Returns a list of all courses contained in this table."""
#         return list(self._lista_insegnamenti)
    
#     def set_lista_insegnamenti(self, lista_ins):
#         """
#         Sets the list of courses for this table.

#         Parameters:
#         - lista_ins: A list of Insegnamento (course) objects.
#         """
#         self._lista_insegnamenti = lista_ins

#     def rimuovi_insegnamenti(self, list_ins):
#         """
#         Removes specific courses from the table.

#         Parameters:
#         - list_ins: A list of courses to be removed based on their names.
#         """
#         self._lista_insegnamenti = list(filter(lambda ins: ins.nome not in [ins2.nome for ins2 in list_ins], self._lista_insegnamenti))
       
#     def __str__(self):
#         """Returns a string representation of the table object."""
#         return f"Nome= {self.nome}"


from constantsScraper import *

# Class representing a course
class Course:

    def __init__(self, period, code, name: str, correlation, credits):
        """
        Initializes a Course object.

        Parameters:
        - period: The academic period (semester or year).
        - code: Unique identifier for the course.
        - name: The name of the course.
        - correlation: Correlation value related to course compatibility.
        - credits: Number of credits assigned to the course.
        """
        self.period = period
        self.code = code
        self.name = name
        self.correlation = correlation
        self.credits = float(credits)  # Convert credits to float for consistency

    def __str__(self):
        """Returns a string representation of the course."""
        return f"Course: {self.name}, Code: {self.code}"

    def __eq__(self, other):
        """Checks if two courses are equal based on their code."""
        return self.code == other.code

    def __le__(self, other):
        """Checks if this course code is less than or equal to another."""
        return self.code <= other.code

    def __lt__(self, other):
        """Checks if this course code is less than another."""
        return self.code < other.code

    def __ge__(self, other):
        """Checks if this course code is greater than or equal to another."""
        return self.code >= other.code

    def __gt__(self, other):
        """Checks if this course code is greater than another."""
        return self.code > other.code

    def __hash__(self):
        """Generates a hash based on the course code (for use in sets/dictionaries)."""
        return hash(self.code)


# Class representing a table (group) of courses
class CourseTable:

    def __init__(self, name: str, year, credits):
        """
        Initializes a CourseTable object.

        Parameters:
        - name: The name of the table (category or elective group).
        - year: The academic year this table is associated with.
        - credits: Total credits associated with this table.
        """
        self.name = name
        self.year = year
        self.credits = float(credits)  # Convert to float for math operations
        self._course_list: list[Course] = []  # Internal list of Course objects

    def get_course_list(self) -> list[Course]:
        """Returns the list of courses in this table."""
        return list(self._course_list)

    def set_course_list(self, course_list):
        """
        Sets the list of courses in the table.

        Parameters:
        - course_list: A list of Course objects to assign to the table.
        """
        self._course_list = course_list

    def remove_courses(self, courses_to_remove):
        """
        Removes specific courses from the table based on their names.

        Parameters:
        - courses_to_remove: A list of Course objects to be removed.
        """
        self._course_list = list(
            filter(lambda course: course.name not in [c.name for c in courses_to_remove], self._course_list)
        )

    def __str__(self):
        """Returns a string representation of the course table."""
        return f"Name = {self.name}"
