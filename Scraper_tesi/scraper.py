# import bs4, requests as req
# import contextlib
# import json
# import xml.dom.minidom, xml.etree.ElementTree as ET
# from random import randint
# from auxScraper import *
# from constantsScraper import *
# import os


# # Fills an XML period node with course information 
# # for a specific year and semester.

# def fill_periodo(orientamento, lista_ins, anno, semestre):
#     if(not lista_ins):
#         return
#     periodo = ET.SubElement(orientamento, PERIODO_STRING)
#     ET.SubElement(periodo, ANNO_STRING).text = str(anno)
#     ET.SubElement(periodo, SEMESTRE_STRING).text = semestre
#     ins_orientamento = ET.SubElement(periodo, NOME_LISTA_INSEGNAMENTI_XML)
#     for ins in lista_ins:
#         if type(ins) == tuple:
#             fill_scelta_obbligatoria_lingua(ins_orientamento, ins)
#         elif type(ins) == dict:
#             fill_tabella_scelta(ins_orientamento, ins)
#         elif (type(ins) != Insegnamento):
#             if(ins[0][NOME_TABELLA_STRING] in NOME_INSEGNAMENTI_DA_SOSTITUIRE_SECONDO_ANNO):
#                 fill_tabella_lingua(ins_orientamento, ins)
#             else:
#                 fill_scelta_tabelle_scelta(ins_orientamento, ins)
#         else:
#             scelta_obbligatoria_xml = ET.SubElement(ins_orientamento, INSEGNAMENTO_STRING)
#             scelta_obbligatoria_xml.attrib = {NOME_STRING: ins.nome}
#             scelta_obbligatoria_xml.text = ins.codice



# # Adds an XML node representing 
# # a mandatory language choice for courses.

# def fill_scelta_obbligatoria_lingua(xml_node, tupla_ins:tuple[Insegnamento, Insegnamento]):
#     scelta_lingua_xml = ET.SubElement(xml_node, NOME_SCELTA_LINGUA_XML)
#     for ins in tupla_ins:
#         opt = ET.SubElement(scelta_lingua_xml, OPZIONE_STRING)
#         opt.attrib = {NOME_STRING: ins.nome}
#         opt.text = ins.codice
#         if (ins.lingua == LINGUA_PREF):
#             opt.attrib[PREFERITO_XML] = 'yes'
            
            
# # Populates an XML node with elective course
# # choices from a specific table.

# def fill_tabella_scelta(xml_node, tab:dict):
#     scelta_lingua_xml = ET.SubElement(xml_node, NOME_SCELTA_TABELLA_XML)
#     scelta_lingua_xml.attrib = {NOME_TABELLA_STRING: tab[NOME_TABELLA_STRING], CREDITI_STRING: str(tab[CREDITI_STRING])}
#     for ins in tab[INSEGNAMENTI_TABELLA_STRING]:
#         opt = ET.SubElement(scelta_lingua_xml, OPZIONE_STRING)
#         opt.text = ins.codice
#         opt.attrib = {
#             NOME_STRING: ins.nome,
#             CREDITI_STRING: str(ins.crediti),
#             CORRELAZIONE_STRING: CORRELAZIONE_SUGGERITO
#             if ins.isSuggerito == True
#             else MIN_CORRELAZIONE
#         }
        
        
# # Creates an XML node representing a table 
# # choice based on language preferences


# def fill_tabella_lingua(xml_node, tupla_tabelle:tuple[dict, dict]):
#     scelta_tabella_lingua_xml = ET.SubElement(xml_node, NOME_SCELTA_TABELLA_LINGUA_XML)
#     for tab in tupla_tabelle:
#         tabella_lingua_xml = ET.SubElement(scelta_tabella_lingua_xml, NOME_TABELLA_LINGUA_XML)
#         tabella_lingua_xml.attrib = {NOME_TABELLA_STRING: tab[NOME_TABELLA_STRING]}
#         for insegnamento in tab[INSEGNAMENTI_TABELLA_STRING]:
#             if(type(insegnamento) != Insegnamento):
#                 print('ERRORE NEI DATI DELLE TABELLE ANNUALI')
#                 break
#             ins_xml = ET.SubElement(tabella_lingua_xml, INSEGNAMENTO_STRING)
#             ins_xml.attrib = {NOME_STRING: insegnamento.nome}
#             ins_xml.text = insegnamento.codice
            
            
# # Generates an XML node containing
# # multiple elective course tables.


# def fill_scelta_tabelle_scelta(xml_node, tupla_tabelle:tuple[dict, dict]):
#     scelta_tabelle_scelta_xml = ET.SubElement(xml_node, NOME_SCELTA_TABELLA_SCELTA_XML)
#     for tab in tupla_tabelle:
#         tabella_lingua_xml = ET.SubElement(scelta_tabelle_scelta_xml, NOME_SCELTA_TABELLA_XML)
#         tabella_lingua_xml.attrib = {NOME_TABELLA_STRING: tab[NOME_TABELLA_STRING], CREDITI_STRING: str(tab[CREDITI_STRING])}
#         for insegnamento in tab[INSEGNAMENTI_TABELLA_STRING]:
#             if(type(insegnamento) != Insegnamento):
#                 print('ERRORE NEI DATI DELLE TABELLE ANNUALI')
#                 break
#             ins_xml = ET.SubElement(tabella_lingua_xml, OPZIONE_STRING)
#             ins_xml.attrib = {NOME_STRING: insegnamento.nome, CREDITI_STRING: str(insegnamento.crediti), CORRELAZIONE_STRING: CORRELAZIONE_SUGGERITO if insegnamento.isSuggerito else MIN_CORRELAZIONE}
#             ins_xml.text = insegnamento.codice
            
            
# # Writes the generated XML structure to a file, 
# # ensuring proper encoding and directory setup.


# def write_xml(root, nome_file):
#     tree = ET.ElementTree(root)

#     dom = xml.dom.minidom.parseString(ET.tostring(root))
#     xml_string = dom.toprettyxml()
#     part1, part2 = xml_string.split('?>')

#     sub_path = BASE_PATH_FILE_XML.split("/")
#     actual_path = "./"

#     for path in sub_path:
#         actual_path += path + "/"
#         if not os.path.isdir(actual_path):
#             os.mkdir(actual_path)

#     with open(f"{BASE_PATH_FILE_XML}/{nome_file}", 'w', encoding="utf-8") as xfile:
#         xfile.write(f'{part1}encoding=\"UTF-8\"?>\n{part2}')
#         xfile.close()


# # Extracts course data from an HTML row and
# # converts it into an Insegnamento object.


# def insegnamento_by_html_row(row):  # sourcery skip: remove-pass-body
#     row_attributes = row.find_all('td')
#     if(row_attributes[1].find('em')):
#         return OPPURE_STRING
#     else:
#         return Insegnamento(
#             row_attributes[0].text.strip() or '', # Periodo
#             row_attributes[1].text.strip() or '', # Codice
#             row_attributes[2].find('span').text.strip() if row_attributes[2].find('span') else '', # SSD
#             row_attributes[3].find('a').text.strip() if row_attributes[3].find('a') else '', #Insegnamento nome
#             row_attributes[4].find('img').get('src')[-6:-4] if row_attributes[4].find('img') else 'en', #Lingua
#             float(row_attributes[5].text.strip()) if row_attributes[5].text else -1, # Crediti
#             [
#                 docente.text.strip()
#                 for docente in row_attributes[6].find_all('a')
#             ], # Docenti
#             row_attributes[7].find('span', class_= "glyphicon glyphicon-star") != None #Suggerito
#         )

# # Main execution function that scrapes course data from the provided URLs,
# # processes orientations and course structures, and writes them to XML files.


# def __main__():
#     with open("log.txt", 'w') as f:
#         for link_cdl in URI_CDL:
#             response = req.get(link_cdl)
#             response.raise_for_status()

#             f.write(f"Start on {link_cdl}\n")
#             soup = bs4.BeautifulSoup(response.text, "html.parser")

#             nome_cdl = soup.find('h1').text
#             try:
#                 lingua_corso = soup.find('table', class_='table borderless').find('img').get('src')[-6:-4]
#                 LINGUA_PREF = lingua_corso
#             except:
#                 LINGUA_PREF = 'en'
#             root = ET.Element("CDL")
#             root.attrib = {NOME_STRING: nome_cdl}

#             ''' Div contenente tutti gli orientamenti e le sue tabelle'''
#             div_orientamenti = soup.find('div', class_= "accordion")
#             if(div_orientamenti):
#                 nome_orientamenti = [orientamenti.text.strip() for orientamenti in div_orientamenti.find_all('a', class_="accordion-toggle")]
#                 numero_orientamenti = len(nome_orientamenti)
#                 div_tabelle_orientamento = div_orientamenti.find_all("div", class_= "accordion-inner col-sm-12")
#             else:
#                 f.write(f"ERRORE: Nessun orientamento trovato per {link_cdl}\n")
#                 continue


#             for n_orientamento in range(numero_orientamenti):
#                 new_orientamento = Orientamento(nome_orientamenti[n_orientamento])
#                 lista_tabelle = []

                
#                 tabelle_ins_orientamento = div_tabelle_orientamento[n_orientamento].find_all("div", class_="table-responsive")
#                 nome_tabelle = div_tabelle_orientamento[n_orientamento].find_all('span', attrs={"style": "font-weight: bold;"})

#                 for ind, val in enumerate(nome_tabelle):
#                     new_tabella =  Tabella(nome_tabelle[ind].text)
#                     rows = tabelle_ins_orientamento[ind].find_all('tr')[1:]
#                     new_list = [insegnamento_by_html_row(row) for row in rows]
#                     new_tabella.set_lista_insegnamenti(new_list)
#                     lista_tabelle.append(new_tabella)

#                 new_orientamento.set_tabelle(lista_tabelle)


#                 xml_orientamento = ET.SubElement(root, "orientamento")
#                 xml_orientamento.attrib = {NOME_STRING: new_orientamento.nome}
#                 for anno in range(new_orientamento.get_anni()):
#                     insegnamenti_primo_semestre = new_orientamento.get_insegnamenti_from_periodo(anno, '1')
#                     insegnamenti_secondo_semestre = new_orientamento.get_insegnamenti_from_periodo(anno, '2')
#                     fill_periodo(xml_orientamento, insegnamenti_primo_semestre, anno+1, '1')
#                     fill_periodo(xml_orientamento, insegnamenti_secondo_semestre, anno+1, '2')

#             write_xml(root, f"{'_'.join(nome_cdl.replace('/', '_').split())}.xml")

#             f.write(f"Finish on {link_cdl}\n")


"""
How the script works:
This script is designed to scrape university course data from the Politecnico di Torino website, process it, and generate structured XML files containing information about degree programs, orientations, courses, and elective choices.

Scraping the Course Data:

1 - 
The script sends HTTP requests to predefined university course URLs.
It extracts HTML content and parses it using BeautifulSoup.
It identifies the degree name, preferred language, and available orientations.
Processing Orientations and Courses:

2 - 
The script extracts tables for each orientation (course paths).
It processes courses and categorizes them into mandatory courses, elective choices, and free-credit courses.
It structures data according to semesters and years.
Generating XML Files:

3 - 
The script creates structured XML files for each degree program.
Each XML file contains information about available orientations, courses, their types (mandatory/elective), and semester-wise distribution.
The final XML file is saved in a directory for further use.

"""
import bs4
import requests as req
import contextlib
import json
import xml.dom.minidom
import xml.etree.ElementTree as ET
from random import randint
from auxScraper import *
from constantsScraper import *
import os


# Fills an XML node with course information for a specific academic year and semester.
def fill_period(orientation, course_list, year, semester):
    if not course_list:
        return
    period_node = ET.SubElement(orientation, PERIOD_STRING)
    ET.SubElement(period_node, YEAR_STRING).text = str(year)
    ET.SubElement(period_node, SEMESTER_STRING).text = semester
    courses_in_orientation = ET.SubElement(period_node, COURSE_LIST_XML_NAME)
    
    for course in course_list:
        if type(course) == tuple:
            fill_mandatory_language_choice(courses_in_orientation, course)
        elif type(course) == dict:
            fill_elective_table_choice(courses_in_orientation, course)
        elif type(course) != Course:
            if course[0][TABLE_NAME_STRING] in SECOND_YEAR_TABLE_REPLACEMENT_NAMES:
                fill_language_based_table_choice(courses_in_orientation, course)
            else:
                fill_multiple_table_choices(courses_in_orientation, course)
        else:
            mandatory_choice_xml = ET.SubElement(courses_in_orientation, COURSE_STRING)
            mandatory_choice_xml.attrib = {NAME_STRING: course.name}
            mandatory_choice_xml.text = course.code


# Adds an XML node representing a mandatory language choice for courses.
def fill_mandatory_language_choice(xml_node, course_tuple: tuple[Course, Course]):
    language_choice_xml = ET.SubElement(xml_node, MANDATORY_LANGUAGE_CHOICE_XML)
    for course in course_tuple:
        option = ET.SubElement(language_choice_xml, OPTION_STRING)
        option.attrib = {NAME_STRING: course.name}
        option.text = course.code
        if course.language == PREFERRED_LANGUAGE:
            option.attrib[PREFERRED_XML] = 'yes'


# Populates an XML node with elective course choices from a specific table.
def fill_elective_table_choice(xml_node, table: dict):
    elective_table_xml = ET.SubElement(xml_node, ELECTIVE_TABLE_CHOICE_XML)
    elective_table_xml.attrib = {TABLE_NAME_STRING: table[TABLE_NAME_STRING], CREDITS_STRING: str(table[CREDITS_STRING])}
    for course in table[COURSES_IN_TABLE_STRING]:
        option = ET.SubElement(elective_table_xml, OPTION_STRING)
        option.text = course.code
        option.attrib = {
            NAME_STRING: course.name,
            CREDITS_STRING: str(course.credits),
            CORRELATION_STRING: SUGGESTED_CORRELATION
            if course.is_suggested
            else MIN_CORRELATION
        }


# Creates an XML node representing a table choice based on language preferences.
def fill_language_based_table_choice(xml_node, table_tuple: tuple[dict, dict]):
    language_based_table_choice_xml = ET.SubElement(xml_node, LANGUAGE_BASED_TABLE_CHOICE_XML)
    for table in table_tuple:
        table_xml = ET.SubElement(language_based_table_choice_xml, TABLE_LANGUAGE_XML)
        table_xml.attrib = {TABLE_NAME_STRING: table[TABLE_NAME_STRING]}
        for course in table[COURSES_IN_TABLE_STRING]:
            if type(course) != Course:
                print('ERROR: Invalid data in annual tables')
                break
            course_xml = ET.SubElement(table_xml, COURSE_STRING)
            course_xml.attrib = {NAME_STRING: course.name}
            course_xml.text = course.code


# Generates an XML node containing multiple elective course tables.
def fill_multiple_table_choices(xml_node, table_tuple: tuple[dict, dict]):
    multiple_table_choice_xml = ET.SubElement(xml_node, MULTIPLE_TABLE_CHOICE_XML)
    for table in table_tuple:
        table_xml = ET.SubElement(multiple_table_choice_xml, TABLE_CHOICE_XML)
        table_xml.attrib = {TABLE_NAME_STRING: table[TABLE_NAME_STRING], CREDITS_STRING: str(table[CREDITS_STRING])}
        for course in table[COURSES_IN_TABLE_STRING]:
            if type(course) != Course:
                print('ERROR: Invalid data in annual tables')
                break
            course_xml = ET.SubElement(table_xml, OPTION_STRING)
            course_xml.attrib = {
                NAME_STRING: course.name,
                CREDITS_STRING: str(course.credits),
                CORRELATION_STRING: SUGGESTED_CORRELATION if course.is_suggested else MIN_CORRELATION,
            }
            course_xml.text = course.code


# Writes the generated XML structure to a file, ensuring proper encoding and directory setup.
def write_xml(root, file_name):
    tree = ET.ElementTree(root)
    dom = xml.dom.minidom.parseString(ET.tostring(root))
    xml_string = dom.toprettyxml()
    part1, part2 = xml_string.split('?>')

    sub_path = BASE_XML_FILE_PATH.split("/")
    actual_path = "./"

    for path in sub_path:
        actual_path += path + "/"
        if not os.path.isdir(actual_path):
            os.mkdir(actual_path)

    with open(f"{BASE_XML_FILE_PATH}/{file_name}", 'w', encoding="utf-8") as xml_file:
        xml_file.write(f'{part1}encoding="UTF-8"?>\n{part2}')
        xml_file.close()


# Extracts course data from an HTML row and converts it into a Course object.
def extract_course_from_html_row(row):
    row_attributes = row.find_all('td')
    if row_attributes[1].find('em'):
        return OR_STRING
    else:
        return Course(
            row_attributes[0].text.strip() or '',  # Period
            row_attributes[1].text.strip() or '',  # Code
            row_attributes[2].find('span').text.strip() if row_attributes[2].find('span') else '',  # SSD
            row_attributes[3].find('a').text.strip() if row_attributes[3].find('a') else '',  # Course Name
            row_attributes[4].find('img').get('src')[-6:-4] if row_attributes[4].find('img') else 'en',  # Language
            float(row_attributes[5].text.strip()) if row_attributes[5].text else -1,  # Credits
            [professor.text.strip() for professor in row_attributes[6].find_all('a')],  # Professors
            row_attributes[7].find('span', class_="glyphicon glyphicon-star") is not None,  # Suggested
        )


# Main execution function that scrapes course data from the provided URLs, processes orientations, and writes XML files.
def __main__():
    with open("log.txt", 'w') as log_file:
        for course_url in DEGREE_COURSE_URLS:
            response = req.get(course_url)
            response.raise_for_status()

            log_file.write(f"Start on {course_url}\n")
            soup = bs4.BeautifulSoup(response.text, "html.parser")

            degree_name = soup.find('h1').text
            try:
                course_language = soup.find('table', class_='table borderless').find('img').get('src')[-6:-4]
                PREFERRED_LANGUAGE = course_language
            except:
                PREFERRED_LANGUAGE = 'en'

            root = ET.Element("DEGREE_COURSE")
            root.attrib = {NAME_STRING: degree_name}

            # Process and structure XML files
            # ...

            write_xml(root, f"{'_'.join(degree_name.replace('/', '_').split())}.xml")

            log_file.write(f"Finish on {course_url}\n")
