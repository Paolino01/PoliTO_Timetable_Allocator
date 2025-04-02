# #Definizioni di classi utilizzate all'interno dello scraper per compattare meglio il codice
# #Nonostante ciò il codice potrebbe decisamente essere strutturato meglio basti vedere le file di replace che ho utilizzato per i nomi
# #quando probabilmente sarebbe bastato aprire i file con encoding='utf-8' ed evitare tutto questo codice inutile
# #Ho provato ad effettuare la modifica ma ci sono troppe cose che perderebbero coerenza, nello file constantScraper ad esempio i nomi sono preimpostati
# #con gli underscore
# from constantsScraper import *

# class Insegnamento:

#     def __init__(self, periodo, codice, ssd, nome:str, lingua, crediti, docenti, suggerito=False):
#         self.periodo = periodo if all(n not in nome.replace(' ', '_') for n in NOME_INSEGNAMENTI_DA_SOSTITUIRE) else '1,2'
#         self.codice = codice
#         self.ssd = ssd
#         self.nome = nome
#         #self.nome = nome.replace(' ', '_').replace("à", "a'").replace("è", "e'").replace("ì", "i'").replace("ò", "o'").replace("ù", "u'").replace('”', '').replace("“", '').replace('–','-').replace('/', '_')
#         self.lingua = lingua
#         self.crediti = crediti
#         self.docenti  = docenti
#         self.isSuggerito = suggerito
    
#     def __str__(self):
#         return f"Insegnamento: {self.nome}, Codice: {self.codice}, Suggerito: {self.isSuggerito}"


# class Tabella:
    
#     def __init__(self, nome:str):
#         self.nome = nome
#         #self.nome = nome.replace(' ', '_').replace(' ', '_').replace("à", "a'").replace("è", "e'").replace("ì", "i'").replace("ò", "o'").replace("ù", "u'").replace('”', '').replace("“", '')
#         self._lista_insegnamenti: list[Insegnamento] = []
#         self._lista_insegnamenti_in_or: list[tuple[Insegnamento, Insegnamento]] = []

#     def _get_lista_insegnamenti(self):
#         return list(self._lista_insegnamenti)
    
#     def _get_lista_insegnamenti_in_or(self):
#         return list(self._lista_insegnamenti_in_or)
    
#     def set_lista_insegnamenti(self, lista_ins):
#         self._lista_insegnamenti = lista_ins
#         if(self._lista_insegnamenti_in_or == []):
#             self._fix_oppure_ins()
#         self._lista_insegnamenti = list(
#             filter(
#                 lambda ins: all(
#                     x not in ins.nome for x in NOME_INSEGNAMENTI_NON_VALIDI
#                 ),
#                 self._lista_insegnamenti,
#             )
#         )

#     def set_lista_insegnamenti_or(self, lista_ins):
#         self._lista_insegnamenti_in_or = lista_ins

#     def set_nome(self, nome):
#         self.nome = nome



#     def get_insegnamenti_semestre(self, semestre) -> list[Insegnamento]:
#         ins_obbligatori = list(filter(lambda ins: semestre in ins.periodo, self._lista_insegnamenti))
#         ins_obbligatori_lingua = list(filter(lambda tuple_ins: semestre in tuple_ins[0].periodo, self._lista_insegnamenti_in_or))
#         return list(ins_obbligatori + ins_obbligatori_lingua)

#     def _trova_oppure_indici(self):
#         return [
#             idx for idx, value in enumerate(self._lista_insegnamenti) if value == OPPURE_STRING
#         ]

#     def _fix_oppure_ins(self):
#         if not (oppure_indici := self._trova_oppure_indici()):
#             return
#         lista_ins = list(self._lista_insegnamenti)
#         lista_ins_or:list[tuple[Insegnamento, Insegnamento]] = []
#         n_non_validi = 0
#         for count, indice in enumerate(oppure_indici):
#             ins1 = self._lista_insegnamenti[indice-1]
#             ins2 = self._lista_insegnamenti[indice+1]
#             offset = 3*count - n_non_validi
#             if(any(x in ins1.nome for x in NOME_INSEGNAMENTI_NON_VALIDI)):
#                 del lista_ins[indice-1-offset : indice+1-offset]
#                 n_non_validi +=1
#             elif(any(x in ins2.nome for x in NOME_INSEGNAMENTI_NON_VALIDI)):
#                 del lista_ins[indice-offset : indice+2-offset]
#                 n_non_validi +=1
#             else:
#                 lista_ins_or.append((ins1, ins2))
#                 del lista_ins[indice-1-offset:indice+2-offset]
#         self._lista_insegnamenti = lista_ins
#         self._lista_insegnamenti_in_or = lista_ins_or
    
#     def __str__(self):
#         return f"""Nome= {self.nome}, Insegnamenti= {
#                 [
#                     str(ins)
#                     for ins in self._lista_insegnamenti
#                 ]
#             }, Insegnamenti_lingua= {
#                 [
#                     f"Insegnamento1= {str(ins[0])} OPPURE Insegnamento2= {str(ins[1])}"
#                     for ins in self._lista_insegnamenti_in_or
#                 ]
#             }"""

# class Orientamento:

#     def __init__(self, nome:str):
#         self.nome = nome
#         #self.nome = nome.replace("à", "a'").replace("è", "e'").replace("ì", "i'").replace("ò", "o'").replace("ù", "u'")
#         self._tabelle_annuali: list[Tabella] = []
#         self._tabelle_scelta: dict[str, Tabella] = {}
#         self._anni = 0

#     def get_tabelle_annuali(self):
#         return list(self._tabelle_annuali)

#     def set_tabelle(self, tabelle:list[Tabella]):
#         self._calculate_anni_corso(tabelle)
#         self._tabelle_annuali = tabelle[:self._anni]
#         for tab in tabelle[self._anni:]:
#             self._tabelle_scelta.update({tab.nome: tab})

#         for nome_tab, tab in self._tabelle_scelta.items():
#             list_ins:list[Insegnamento] = tab._get_lista_insegnamenti()
#             for ind, ins in enumerate(tab._get_lista_insegnamenti()):
#                 if(ins.nome in self._tabelle_scelta.keys()):
#                     list_ins = list_ins[:ind] + self._tabelle_scelta[ins.nome]._get_lista_insegnamenti() + list_ins[ind+1:]
#                     self._tabelle_scelta[nome_tab].set_nome(f"{nome_tab}({ins.nome.replace('°','')})")
#             self._tabelle_scelta[nome_tab].set_lista_insegnamenti(list_ins)

#         #if (self._anni >= 2):
#         #    self._fix_tabelle_annuali()

#     def _fix_tabelle_annuali(self):
#         tab = self._tabelle_annuali[1]
#         list_ins_or:list[tuple[Insegnamento,Insegnamento]] = tab._get_lista_insegnamenti_in_or()
#         list_ins:list[Insegnamento] = tab._get_lista_insegnamenti()
#         modifica = False
#         for ind, tupla in enumerate(list_ins_or):
#             if (all(nome in NOMI_TABELLE_SCELTA for nome in [tupla[0].nome, tupla[1].nome])):
#                 list_ins.extend((tupla[0], tupla[1]))
#                 del list_ins_or[ind]
#                 modifica = True
#                 break
#         if(modifica):
#             tab.set_lista_insegnamenti(list_ins)
#             tab.set_lista_insegnamenti_or(list_ins_or)
            
            
            
            

        
#     def get_anni(self):
#         return self._anni

#     def get_insegnamenti_from_periodo(self, anno, semestre):
#         insegnamenti_periodo = self._tabelle_annuali[anno].get_insegnamenti_semestre(semestre)
#         for indice, insegnamento in enumerate(insegnamenti_periodo):
#             if(type(insegnamento) == tuple and insegnamento[0].nome in NOMI_TABELLE_SCELTA):
#                 try:
#                     insegnamenti_periodo[indice] = [
#                         {
#                             NOME_TABELLA_STRING:insegnamento[0].nome,
#                             CREDITI_STRING: insegnamento[0].crediti,
#                             INSEGNAMENTI_TABELLA_STRING: self._tabelle_scelta[insegnamento[0].nome].get_insegnamenti_semestre(semestre)
#                         },
#                         {
#                             NOME_TABELLA_STRING:insegnamento[1].nome,
#                             CREDITI_STRING: insegnamento[1].crediti,
#                             INSEGNAMENTI_TABELLA_STRING: self._tabelle_scelta[insegnamento[1].nome].get_insegnamenti_semestre(semestre)
#                         },
#                     ]
#                 except KeyError:
#                     print("ERR: Tabella non esistente")
#                     print(anno, semestre, f"\nTabelle che sto considerando: ['{insegnamento[0].nome}', '{insegnamento[1].nome}']\nTabelle che ho: ", list(self._tabelle_scelta.keys()))
#                     if(insegnamento[0].nome in self._tabelle_scelta):
#                         lista_ins_scelta = self._tabelle_scelta[insegnamento[0].nome].get_insegnamenti_semestre(semestre)
#                         insegnamenti_periodo[indice] = {NOME_TABELLA_STRING:self._tabelle_scelta[insegnamento[0].nome].nome, CREDITI_STRING: insegnamento[0].crediti, INSEGNAMENTI_TABELLA_STRING: lista_ins_scelta}
#                     else:  
#                         lista_ins_scelta = self._tabelle_scelta[insegnamento[1].nome].get_insegnamenti_semestre(semestre)
#                         insegnamenti_periodo[indice] = {NOME_TABELLA_STRING:self._tabelle_scelta[insegnamento[1].nome].nome, CREDITI_STRING: insegnamento[1].crediti, INSEGNAMENTI_TABELLA_STRING: lista_ins_scelta}
#             if(type(insegnamento) == tuple or insegnamento.nome not in self._tabelle_scelta):
#                 continue
#             if(insegnamento.nome not in self._tabelle_scelta.keys()):
#                 print("ERRORE NON DOVREBBE SUCCEDERE")
#                 continue
#             lista_ins_scelta = self._tabelle_scelta[insegnamento.nome].get_insegnamenti_semestre(semestre)
#             insegnamenti_periodo[indice] = {NOME_TABELLA_STRING:self._tabelle_scelta[insegnamento.nome].nome, CREDITI_STRING: insegnamento.crediti, INSEGNAMENTI_TABELLA_STRING: lista_ins_scelta}
#         return insegnamenti_periodo


#     def _calculate_anni_corso(self, tabelle:list[Tabella]):
#         nAnni = sum(
#             any(
#                 (
#                     tab.nome.startswith(f'{str(anno)}° anno')
#                     for tab in tabelle
#                 )
#             )
#             for anno in range(1, 4)
#         )
#         self._anni = nAnni

#     def __str__(self) -> str:
#         return f"""Orientamento: {self.nome}, Numero_tabelle: {len(self._tabelle_annuali)}|{len(self._tabelle_scelta)}, Numero_anni: {self._anni}
# Tabelle annuali: {[str(tab) for tab in self._tabelle_annuali]}
# Tabelle a scelta: {self._tabelle_scelta}"""


from constantsScraper import *

# Class representing a course
class Course:

    def __init__(self, period, code, ssd, name: str, language, credits, instructors, suggested=False):
        """
        Initializes a Course object.

        Parameters:
        - period: The academic period (e.g., semester or year).
        - code: Unique course code.
        - ssd: Scientific disciplinary sector.
        - name: Course name.
        - language: Language of instruction.
        - credits: Number of credits.
        - instructors: List of instructors.
        - suggested: Boolean flag indicating if the course is suggested.
        """
        self.period = period if all(n not in name.replace(' ', '_') for n in COURSES_TO_REPLACE) else '1,2'
        self.code = code
        self.ssd = ssd
        self.name = name
        self.language = language
        self.credits = credits
        self.instructors = instructors
        self.isSuggested = suggested

    def __str__(self):
        return f"Course: {self.name}, Code: {self.code}, Suggested: {self.isSuggested}"


# Class representing a table of grouped courses
class CourseTable:

    def __init__(self, name: str):
        self.name = name
        self._courses: list[Course] = []
        self._courses_in_or_condition: list[tuple[Course, Course]] = []

    def get_courses(self):
        return list(self._courses)

    def get_courses_in_or(self):
        return list(self._courses_in_or_condition)

    def set_courses(self, course_list):
        self._courses = course_list
        if not self._courses_in_or_condition:
            self._process_or_conditions()
        self._courses = list(
            filter(
                lambda course: all(
                    x not in course.name for x in INVALID_COURSE_NAMES
                ),
                self._courses,
            )
        )

    def set_courses_in_or(self, or_list):
        self._courses_in_or_condition = or_list

    def set_name(self, name):
        self.name = name

    def get_courses_for_semester(self, semester) -> list[Course]:
        required_courses = list(filter(lambda course: semester in course.period, self._courses))
        language_courses = list(filter(lambda pair: semester in pair[0].period, self._courses_in_or_condition))
        return list(required_courses + language_courses)

    def _find_or_indices(self):
        return [idx for idx, value in enumerate(self._courses) if value == OR_STRING]

    def _process_or_conditions(self):
        if not (or_indices := self._find_or_indices()):
            return
        course_list = list(self._courses)
        or_pairs: list[tuple[Course, Course]] = []
        invalid_count = 0
        for count, index in enumerate(or_indices):
            course1 = self._courses[index - 1]
            course2 = self._courses[index + 1]
            offset = 3 * count - invalid_count
            if any(x in course1.name for x in INVALID_COURSE_NAMES):
                del course_list[index - 1 - offset : index + 1 - offset]
                invalid_count += 1
            elif any(x in course2.name for x in INVALID_COURSE_NAMES):
                del course_list[index - offset : index + 2 - offset]
                invalid_count += 1
            else:
                or_pairs.append((course1, course2))
                del course_list[index - 1 - offset : index + 2 - offset]
        self._courses = course_list
        self._courses_in_or_condition = or_pairs

    def __str__(self):
        return f"""Name = {self.name}, Courses = {
                [
                    str(course)
                    for course in self._courses
                ]
            }, Language Option Courses = {
                [
                    f"Course1 = {str(pair[0])} OR Course2 = {str(pair[1])}"
                    for pair in self._courses_in_or_condition
                ]
            }"""


# Class representing an orientation/specialization
class Orientation:

    def __init__(self, name: str):
        self.name = name
        self._yearly_tables: list[CourseTable] = []
        self._elective_tables: dict[str, CourseTable] = {}
        self._years = 0

    def get_yearly_tables(self):
        return list(self._yearly_tables)

    def set_tables(self, tables: list[CourseTable]):
        self._calculate_years_in_program(tables)
        self._yearly_tables = tables[:self._years]
        for table in tables[self._years:]:
            self._elective_tables.update({table.name: table})

        for table_name, table in self._elective_tables.items():
            course_list: list[Course] = table.get_courses()
            for idx, course in enumerate(course_list):
                if course.name in self._elective_tables:
                    course_list = course_list[:idx] + self._elective_tables[course.name].get_courses() + course_list[idx + 1:]
                    self._elective_tables[table_name].set_name(f"{table_name}({course.name.replace('°', '')})")
            self._elective_tables[table_name].set_courses(course_list)

    def _calculate_years_in_program(self, tables: list[CourseTable]):
        total_years = sum(
            any(
                (
                    table.name.startswith(f'{str(year)}° year')
                    for table in tables
                )
            )
            for year in range(1, 4)
        )
        self._years = total_years

    def get_courses_for_period(self, year, semester):
        period_courses = self._yearly_tables[year].get_courses_for_semester(semester)
        for idx, course in enumerate(period_courses):
            if isinstance(course, tuple) or course.name not in self._elective_tables:
                continue
            elective_courses = self._elective_tables[course.name].get_courses_for_semester(semester)
            period_courses[idx] = {
                TABLE_NAME_STRING: self._elective_tables[course.name].name,
                CREDITS_STRING: course.credits,
                TABLE_COURSES_STRING: elective_courses
            }
        return period_courses

    def __str__(self) -> str:
        return f"""Orientation: {self.name}, Number of tables: {len(self._yearly_tables)}|{len(self._elective_tables)}, Years: {self._years}
Yearly Tables: {[str(tab) for tab in self._yearly_tables]}
Elective Tables: {self._elective_tables.keys()}"""
