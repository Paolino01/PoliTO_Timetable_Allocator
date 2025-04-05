# from dbAPI import dbAPI
# import constantsScraper as cs
# import xml.etree.ElementTree as et
    
# db:dbAPI = dbAPI(cs.PATH_DB)

# tuple_file_nomecdl_tipocdl = [
#     ("CDL_XML_A_ACC_2024/Corso_di_Laurea_in_Electronic_and_communications_engineering_(ingegneria_elettronica_e_delle_comunicazioni)_(Torino).xml", "ELECTRONIC AND COMMUNICATIONS ENGINEERING (INGEGNERIA ELETTRONICA E DELLE COMUNICAZIONI)", "1"),
#     ("CDL_XML_A_ACC_2024/Corso_di_Laurea_in_Ingegneria_del_cinema_e_dei_mezzi_di_comunicazione_(Torino).xml", "INGEGNERIA DEL CINEMA E DEI MEZZI DI COMUNICAZIONE", "1"),
#     ("CDL_XML_A_ACC_2024/Corso_di_Laurea_in_Ingegneria_elettronica_(Torino).xml", "INGEGNERIA ELETTRONICA", "1"),
#     ("CDL_XML_A_ACC_2024/Corso_di_Laurea_in_Ingegneria_fisica_(Torino).xml","INGEGNERIA FISICA", "1"),
#     ("CDL_XML_A_ACC_2024/Corso_di_Laurea_in_Ingegneria_informatica_(Torino).xml", "INGEGNERIA INFORMATICA", "1"),
#     ("CDL_XML_A_ACC_2024/Corso_di_Laurea_in_Ingegneria_informatica_(computer_engineering)_(Torino).xml", "INGEGNERIA INFORMATICA (COMPUTER ENGINEERING)", "1"),
#     ("CDL_XML_A_ACC_2024/Corso_di_Laurea_Magistrale_in_Agritech_engineering_(Torino).xml", "AGRITECH ENGINEERING", "Z"),
#     ("CDL_XML_A_ACC_2024/Corso_di_Laurea_Magistrale_in_Communications_engineering_(Torino).xml", "COMMUNICATIONS ENGINEERING", "Z"),
#     ("CDL_XML_A_ACC_2024/Corso_di_Laurea_Magistrale_in_Cybersecurity__(Torino).xml", "CYBERSECURITY", "Z"),
#     ("CDL_XML_A_ACC_2024/Corso_di_Laurea_Magistrale_in_Data_science_and_engineering_(Torino).xml", "DATA SCIENCE AND ENGINEERING", "Z"),
#     ("CDL_XML_A_ACC_2024/Corso_di_Laurea_Magistrale_in_Ict_for_smart_societies_(ict_per_la_societa'_del_futuro)_(Torino).xml", "ICT FOR SMART SOCIETIES (ICT PER LA SOCIETA' DEL FUTURO)", "Z"),
#     ("CDL_XML_A_ACC_2024/Corso_di_Laurea_Magistrale_in_Ingegneria_del_cinema_e_dei_mezzi_di_comunicazione_(Torino).xml", "INGEGNERIA DEL CINEMA E DEI MEZZI DI COMUNICAZIONE", "Z"),
#     ("CDL_XML_A_ACC_2024/Corso_di_Laurea_Magistrale_in_Ingegneria_elettronica_(electronic_engineering)_(Torino).xml", "INGEGNERIA ELETTRONICA (ELECTRONIC ENGINEERING)", "Z"),
#     ("CDL_XML_A_ACC_2024/Corso_di_Laurea_Magistrale_in_Ingegneria_informatica_(computer_engineering)_(Torino).xml", "INGEGNERIA INFORMATICA (COMPUTER ENGINEERING)", "Z"),
#     ("CDL_XML_A_ACC_2024/Corso_di_Laurea_Magistrale_in_Mechatronic_engineering_(ingegneria_meccatronica)_(Torino).xml", "MECHATRONIC ENGINEERING (INGEGNERIA MECCATRONICA)", "Z"),
#     ("CDL_XML_A_ACC_2024/Corso_di_Laurea_Magistrale_in_Nanotechnologies_for_icts_(nanotecnologie_per_le_ict)_(Torino_Grenoble_Losanna).xml", "NANOTECHNOLOGIES FOR ICTs (NANOTECNOLOGIE PER LE ICT)", "Z"),
#     ("CDL_XML_A_ACC_2024/Corso_di_Laurea_Magistrale_in_Physics_of_complex_systems_(fisica_dei_sistemi_complessi)_(Torino_Trieste_Parigi).xml", "PHYSICS OF COMPLEX SYSTEMS (FISICA DEI SISTEMI COMPLESSI)", "Z"),
#     ("CDL_XML_A_ACC_2024/Corso_di_Laurea_Magistrale_in_Quantum_engineering_(Torino).xml", "QUANTUM ENGINEERING", "Z"),
# ]

# for t in tuple_file_nomecdl_tipocdl:
#     try:
#         xml = et.parse(t[0])
#     except:
#         continue
#     cdl = t[1]
#     tipoCdl = t[2]
#     root = xml.getroot()
#     xml_orientamenti = root.findall("orientamento")

#     for xml_orient in xml_orientamenti:
#         orient_name = xml_orient.get("nome")
#         if "Mondovi" in orient_name:
#             orient_name = "Primo anno sede di Mondovì"
#         xml_periodi = xml_orient.findall("periodo")

#         for xml_periodo in xml_periodi:
#             semestre = xml_periodo.find("semestre").text
#             anno = xml_periodo.find("anno").text
#             if(semestre == "2"):
#                 continue
#             periodo = f"{anno}-{semestre}"
#             xml_insegnamenti = xml_periodo.find("insegnamenti_in_orientamento")

#             xml_obbligatori = xml_insegnamenti.findall("insegnamento")
#             for ins in xml_obbligatori:
#                 id_inc = db.get_ID_INC_from_codIns(ins.text)
#                 for i in id_inc:
#                     db.update_InsegnamentiInOrientamento(orient_name, cdl, tipoCdl, periodo, "Obbligatorio", i[0])

#             xml_scelte_lingua = xml_insegnamenti.findall("scelta_obbligatoria_lingua")
#             for xml_scelta_lingua in xml_scelte_lingua:
#                 xml_opzioni = xml_scelta_lingua.findall("opzione")
#                 for opzione in xml_opzioni:
#                     id_inc = db.get_ID_INC_from_codIns(opzione.text)
#                     for i in id_inc:
#                         db.update_InsegnamentiInOrientamento(orient_name, cdl, tipoCdl, periodo, "Obbligatorio_a_scelta", i[0])
            
#             xml_scelte_tabella = xml_insegnamenti.findall("scelta_tabella")
#             for xml_scelta_tabella in xml_scelte_tabella:
#                 xml_opzioni = xml_scelta_tabella.findall("opzione")
#                 if len(xml_opzioni) > 3:
#                     for opzione in xml_opzioni:
#                         corr = opzione.get("correlazione")
#                         tipo = "Credito_libero_consigliato" if corr == "95" else "Tabella_a_scelta"
#                         id_inc = db.get_ID_INC_from_codIns(opzione.text)
#                         for i in id_inc:
#                             db.update_InsegnamentiInOrientamento(orient_name, cdl, tipoCdl, periodo, tipo, i[0])
#                 else:
#                     for opzione in xml_opzioni:
#                         id_inc = db.get_ID_INC_from_codIns(opzione.text)
#                         for i in id_inc:
#                             db.update_InsegnamentiInOrientamento(orient_name, cdl, tipoCdl, periodo, "Obbligatorio_a_scelta", i[0])
            
#             xml_scelta_tabella_lingua = xml_insegnamenti.find("scelta_tabella_lingua")
#             if xml_scelta_tabella_lingua == None:
#                 continue
#             for tabella_lingua in xml_scelta_tabella_lingua:
#                 for ins in tabella_lingua:
#                     id_inc = db.get_ID_INC_from_codIns(ins.text)
#                     for i in id_inc:
#                         db.update_InsegnamentiInOrientamento(orient_name, cdl, tipoCdl, periodo, "Obbligatorio", i[0])


"""

This script processes XML files containing information about degree programs (CDL - "Corso di Laurea") and their respective orientations (tracks), periods (semesters and years), and courses.

The script performs the following tasks:

Connects to an SQLite database using dbAPI to update information about courses.

Reads multiple XML files that contain data about different degree programs.

Extracts details such as:

Orientation (Orientamento)

Academic Year (Anno) and Semester (Semestre)

Courses (Insegnamenti)

Classifies courses based on their type:

Obbligatorio (Mandatory courses)

Obbligatorio_a_scelta (Elective courses)

Credito_libero_consigliato (Recommended free credit courses)

Updates the database with this extracted data.

"""


from dbAPI import dbAPI
import constantsScraper as cs
import xml.etree.ElementTree as et

# Establish a connection to the database
db: dbAPI = dbAPI(cs.PATH_DB)

# List of XML files containing degree program data
# Each tuple contains:
# - XML file path
# - Degree program name
# - Degree type (1 = Bachelor's, Z = Master's)

tuple_file_nomecdl_tipocdl = [
    ("CDL_XML_A_ACC_2024/Corso_di_Laurea_in_Electronic_and_communications_engineering_(ingegneria_elettronica_e_delle_comunicazioni)_(Torino).xml", 
     "ELECTRONIC AND COMMUNICATIONS ENGINEERING (INGEGNERIA ELETTRONICA E DELLE COMUNICAZIONI)", "1"),
    ("CDL_XML_A_ACC_2024/Corso_di_Laurea_in_Ingegneria_del_cinema_e_dei_mezzi_di_comunicazione_(Torino).xml", 
     "INGEGNERIA DEL CINEMA E DEI MEZZI DI COMUNICAZIONE", "1"),
    ("CDL_XML_A_ACC_2024/Corso_di_Laurea_Magistrale_in_Quantum_engineering_(Torino).xml", 
     "QUANTUM ENGINEERING", "Z"),
]

# Process each XML file
for t in tuple_file_nomecdl_tipocdl:
    try:
        # Parse the XML file
        xml = et.parse(t[0])
    except:
        continue  # Skip if the file cannot be read

    # Extract degree program name and type
    cdl = t[1]
    tipoCdl = t[2]
    root = xml.getroot()
    
    # Find all orientations (tracks) in the degree program
    xml_orientamenti = root.findall("orientamento")

    for xml_orient in xml_orientamenti:
        # Get the orientation name
        orient_name = xml_orient.get("nome")

        # Rename "Mondovì" track to a standard name
        if "Mondovi" in orient_name:
            orient_name = "Primo anno sede di Mondovì"

        # Find all periods (years and semesters) in the orientation
        xml_periodi = xml_orient.findall("periodo")

        for xml_periodo in xml_periodi:
            # Extract semester and year
            semestre = xml_periodo.find("semestre").text
            anno = xml_periodo.find("anno").text

            # Only process first semester courses (skip second semester)
            if semestre == "2":
                continue

            # Format period as "year-semester" (e.g., "1-1")
            periodo = f"{anno}-{semestre}"

            # Find all courses (insegnamenti) within the period
            xml_insegnamenti = xml_periodo.find("insegnamenti_in_orientamento")

            # **1. Process mandatory courses**
            xml_obbligatori = xml_insegnamenti.findall("insegnamento")
            for ins in xml_obbligatori:
                # Get the unique course ID from the database
                id_inc = db.get_ID_INC_from_codIns(ins.text)
                for i in id_inc:
                    # Update course as "Mandatory" in the database
                    db.update_InsegnamentiInOrientamento(orient_name, cdl, tipoCdl, periodo, "Obbligatorio", i[0])

            # **2. Process mandatory language-based course selections**
            xml_scelte_lingua = xml_insegnamenti.findall("scelta_obbligatoria_lingua")
            for xml_scelta_lingua in xml_scelte_lingua:
                xml_opzioni = xml_scelta_lingua.findall("opzione")
                for opzione in xml_opzioni:
                    id_inc = db.get_ID_INC_from_codIns(opzione.text)
                    for i in id_inc:
                        # Update course as "Mandatory Elective" in the database
                        db.update_InsegnamentiInOrientamento(orient_name, cdl, tipoCdl, periodo, "Obbligatorio_a_scelta", i[0])

            # **3. Process elective course tables**
            xml_scelte_tabella = xml_insegnamenti.findall("scelta_tabella")
            for xml_scelta_tabella in xml_scelte_tabella:
                xml_opzioni = xml_scelta_tabella.findall("opzione")

                # If the table has more than 3 options, classify courses differently
                if len(xml_opzioni) > 3:
                    for opzione in xml_opzioni:
                        corr = opzione.get("correlazione")
                        # If correlation = 95, classify as "Recommended Free Credit"
                        tipo = "Credito_libero_consigliato" if corr == "95" else "Tabella_a_scelta"
                        id_inc = db.get_ID_INC_from_codIns(opzione.text)
                        for i in id_inc:
                            db.update_InsegnamentiInOrientamento(orient_name, cdl, tipoCdl, periodo, tipo, i[0])
                else:
                    for opzione in xml_opzioni:
                        id_inc = db.get_ID_INC_from_codIns(opzione.text)
                        for i in id_inc:
                            # Update course as "Mandatory Elective"
                            db.update_InsegnamentiInOrientamento(orient_name, cdl, tipoCdl, periodo, "Obbligatorio_a_scelta", i[0])

            # **4. Process language-based course tables**
            xml_scelta_tabella_lingua = xml_insegnamenti.find("scelta_tabella_lingua")
            if xml_scelta_tabella_lingua is None:
                continue

            for tabella_lingua in xml_scelta_tabella_lingua:
                for ins in tabella_lingua:
                    id_inc = db.get_ID_INC_from_codIns(ins.text)
                    for i in id_inc:
                        # Update course as "Mandatory"
                        db.update_InsegnamentiInOrientamento(orient_name, cdl, tipoCdl, periodo, "Obbligatorio", i[0])
