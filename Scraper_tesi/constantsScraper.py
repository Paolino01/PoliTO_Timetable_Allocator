# # declare constants

# ### JUST STRINGS
# ### Non so quanto questa cosa sia utile, credo di aver seguito le orme di kotlin dove l'IDE diceva di non utilizzare stringhe nel codice
# ### ma definirle in un file a parte
# OPPURE_STRING = "Oppure"
# PERIODO_STRING = "periodo"
# ANNO_STRING = "anno"
# SEMESTRE_STRING = "semestre"
# INSEGNAMENTO_STRING = "insegnamento"
# CORRELAZIONE_STRING = "correlazione"
# NOME_STRING = "nome"
# NOME_TABELLA_STRING = "nome_tabella"
# CREDITI_STRING = "crediti"
# INSEGNAMENTI_TABELLA_STRING = "insegnamenti_tabella"
# OPZIONE_STRING = "opzione"

# ### VARIABILI
# # A posteriori ho dubbi sul fatto che questo fosse necessario, ricordo che avevo il nome delle tabelle che riuscivo a ricavare da un orientamento
# # quindi non so perche' non sostituivo direttamente qualsiasi insegnamento che aveva un nome uguale ad una delle tabelle trovate
# LINGUA_PREF = "en"
# NOME_INSEGNAMENTI_NON_VALIDI = ['Tesi', 'Thesis', 'Prova_finale', 'Final_Project', 'Final_project', 'Tirocinio', '1st_Year', '2nd_Year', 'Internship']
# NOME_INSEGNAMENTI_DA_SOSTITUIRE = ['Insegnamento_a_scelta', 'Free_choice', 'Free_Choice', 'Choice_from', 'Crediti_liberi', 'sfide_globali_-_Intraprendenti', 'Free_ECTS_credits', 'Tabella_1', 'Tabella_2', 'Tabella_3', 'Tabella_4', 'Elective_course']
# NOMI_TABELLE_SCELTA = ['2nd_year_taught_in_English', 'Secondo_anno_erogato_in_italiano', 'Challenge', 'Crediti_liberi']
# NOME_INSEGNAMENTI_DA_SOSTITUIRE_TABELLE_SCELTA = ['Challenge', 'Crediti_liberi']
# NOME_INSEGNAMENTI_DA_SOSTITUIRE_SECONDO_ANNO = ['2nd_year_taught_in_English', 'Secondo_anno_erogato_in_italiano']

# NOME_TABELLE_CON_CREDITI_LIBERI = ['Crediti_liberi', 'Free_ECTS_credits']


# ### XML STRINGS 
# NOME_LISTA_INSEGNAMENTI_XML = "insegnamenti_in_orientamento"
# NOME_INSEGNAMENTO_OBBLIGATORIO_XML = "scelta_obbligatoria"
# NOME_SCELTA_LINGUA_XML = "scelta_obbligatoria_lingua"
# NOME_SCELTA_TABELLA_XML = "scelta_tabella"
# NOME_SCELTA_TABELLA_LINGUA_XML = "scelta_tabella_lingua"
# NOME_SCELTA_TABELLA_SCELTA_XML = "scelta_tabella_scelta"
# NOME_TABELLA_LINGUA_XML = "tabella_lingua"
# PREFERITO_XML = "preferito_lingua"

# ### VALORI CORRELAZIONE
# MAX_CORRELAZIONE = '100'
# MIN_CORRELAZIONE = '20'
# CORRELAZIONE_SUGGERITO = '95'
# CORRELAZIONE_OBBLIGATORI_LINGUE_DIVERSE = '90'

# ### uri cdl
# URI_CDL = [
#     'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=37&p_cds=930', # Magistrale Communications
#     'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=37&p_cds=320', # Magistrale Data Science
#     'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=37&p_cds=17', # Triennale Elettronica e Communications
#     'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=37&p_cds=20', # Magistrale ICT
#     'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=37&p_cds=21', # Triennale Cinema
#     'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=37&p_cds=18', # Magistrale Informatica
#     'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=32&p_cds=137', # Quantum
#     'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=37&p_cds=22', # Magistrale Cinema
#     'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=37&p_cds=1', # Triennale Elettronica
#     'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=37&p_cds=13', # Magistrale Elettronica
#     'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=37&p_cds=9', # Triennale Fisica
#     'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=37&p_cds=3', # Triennale Informatica
#     'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=37&p_cds=55', # Magistrale Meccatronica
#     'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=37&p_cds=23', # Magistrale Nanotecnologie
#     'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=37&p_cds=24', # Magistrale Fisica Sistemi Complessi
#     'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=37&p_cds=10', # Triennale ing inf inglese
#     'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=32&p_cds=138', # Mag Cybersec
#     'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=32&p_cds=136', # Agritech engineering
#     'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=37&p_cds=17', # Magistrale eletronic e communications
#     'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=37&p_cds=30 ', # magistrale communications e computer network
# ]

# URI_CDL2 = [
#     'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2023&p_sdu=37&p_cds=930', # Magistrale Communications
#     'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2023&p_sdu=37&p_cds=320', # Magistrale Data Science
#     'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2023&p_sdu=37&p_cds=17', # Triennale Elettronica e Communications
#     'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2023&p_sdu=37&p_cds=20', # Magistrale ICT
#     'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2023&p_sdu=37&p_cds=21', # Triennale Cinema
#     'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_coorte=2022&p_sdu=37&p_cds=18', # Magistrale Informatica
#     'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2023&p_sdu=37&p_cds=22', # Magistrale Cinema
#     'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2023&p_sdu=37&p_cds=1', # Triennale Elettronica
#     'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2023&p_sdu=37&p_cds=13', # Magistrale Elettronica
#     'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2023&p_sdu=37&p_cds=9', # Triennale Fisica
#     'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2023&p_sdu=37&p_cds=3', # Triennale Informatica
#     'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2023&p_sdu=37&p_cds=55', # Magistrale Meccatronica
#     'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2023&p_sdu=37&p_cds=23', # Magistrale Nanotecnologie
#     'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2023&p_sdu=37&p_cds=24', # Magistrale Fisica Sistemi Complessi
#     'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2023&p_sdu=37&p_cds=10', # Triennale ing inf inglese
# ]

# ### Cartelle file
# __BASE_PATH = "./TestData4"
# BASE_PATH_FILE_XML = f'{__BASE_PATH}/CDL_XML_A_ACC_2024'
# BASE_PATH_FILE_EXCEL = f'{__BASE_PATH}/CDL_EXCELS_A_ACC_2024'
# BASE_PATH_FILE_RESULT_XML = f'{__BASE_PATH}/Results'
# PATH_DB = "./Data/GoodDB.db"
# SEMESTRE = 1 #SCELTA TRA 1 O 2




# **********************************************************************
# **********************************************************************
# **********************************************************************
# **********************************************************************
# **********************************************************************
# **********************************************************************
# **********************************************************************
# **********************************************************************
# **********************************************************************
# **********************************************************************
# **********************************************************************


# ENGLISH COMMENT

# Declare constants

### JUST STRINGS
### Not sure how useful this is, probably followed Kotlin's pattern where the IDE suggested avoiding direct string literals in code
### and defining them separately in a constants file instead.


OPPURE_STRING = "Oppure"
PERIODO_STRING = "periodo"
ANNO_STRING = "anno"
SEMESTRE_STRING = "semestre"
INSEGNAMENTO_STRING = "insegnamento"
CORRELAZIONE_STRING = "correlazione"
NOME_STRING = "nome"
NOME_TABELLA_STRING = "nome_tabella"
CREDITI_STRING = "crediti"
INSEGNAMENTI_TABELLA_STRING = "insegnamenti_tabella"
OPZIONE_STRING = "opzione"

### VARIABLES
# In hindsight, I'm unsure if this was necessary. I recall that I could extract table names from an orientation,
# so I'm not sure why I didn't directly replace any course with a name matching one of the extracted tables.
LINGUA_PREF = "en"
NOME_INSEGNAMENTI_NON_VALIDI = ['Tesi', 'Thesis', 'Prova_finale', 'Final_Project', 'Final_project', 'Tirocinio', '1st_Year', '2nd_Year', 'Internship']
NOME_INSEGNAMENTI_DA_SOSTITUIRE = ['Insegnamento_a_scelta', 'Free_choice', 'Free_Choice', 'Choice_from', 'Crediti_liberi', 'sfide_globali_-_Intraprendenti', 'Free_ECTS_credits', 'Tabella_1', 'Tabella_2', 'Tabella_3', 'Tabella_4', 'Elective_course']
NOMI_TABELLE_SCELTA = ['2nd_year_taught_in_English', 'Secondo_anno_erogato_in_italiano', 'Challenge', 'Crediti_liberi']
NOME_INSEGNAMENTI_DA_SOSTITUIRE_TABELLE_SCELTA = ['Challenge', 'Crediti_liberi']
NOME_INSEGNAMENTI_DA_SOSTITUIRE_SECONDO_ANNO = ['2nd_year_taught_in_English', 'Secondo_anno_erogato_in_italiano']

NOME_TABELLE_CON_CREDITI_LIBERI = ['Crediti_liberi', 'Free_ECTS_credits']

### XML STRINGS
NOME_LISTA_INSEGNAMENTI_XML = "insegnamenti_in_orientamento"
NOME_INSEGNAMENTO_OBBLIGATORIO_XML = "scelta_obbligatoria"
NOME_SCELTA_LINGUA_XML = "scelta_obbligatoria_lingua"
NOME_SCELTA_TABELLA_XML = "scelta_tabella"
NOME_SCELTA_TABELLA_LINGUA_XML = "scelta_tabella_lingua"
NOME_SCELTA_TABELLA_SCELTA_XML = "scelta_tabella_scelta"
NOME_TABELLA_LINGUA_XML = "tabella_lingua"
PREFERITO_XML = "preferito_lingua"

### CORRELATION VALUES
MAX_CORRELAZIONE = '100'  # Maximum correlation value
MIN_CORRELAZIONE = '20'   # Minimum correlation value
CORRELAZIONE_SUGGERITO = '95'  # Suggested correlation value
CORRELAZIONE_OBBLIGATORI_LINGUE_DIVERSE = '90'  # Correlation for mandatory courses in different languages

### Course URLs
# These are links to course descriptions on the university website.
# Used for scraping or updating course data dynamically.
URI_CDL = [
    'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=37&p_cds=930',  # Master's in Communications
    'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=37&p_cds=320',  # Master's in Data Science
    'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=37&p_cds=17',   # Bachelor's in Electronics and Communications
    'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=37&p_cds=20',   # Master's in ICT
    'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=37&p_cds=21',   # Bachelor's in Cinema
    'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=37&p_cds=18',   # Master's in Computer Engineering
    'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=32&p_cds=137',  # Quantum Engineering
    'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=37&p_cds=22',   # Master's in Cinema
    'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=37&p_cds=1',    # Bachelor's in Electronics
    'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=37&p_cds=13',   # Master's in Electronics
    'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=37&p_cds=9',    # Bachelor's in Physics
    'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=37&p_cds=3',    # Bachelor's in Computer Science
    'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=37&p_cds=55',   # Master's in Mechatronics
    'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=37&p_cds=23',   # Master's in Nanotechnology
    'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=37&p_cds=24',   # Master's in Physics of Complex Systems
    'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=37&p_cds=10',   # Bachelor's in Computer Engineering (English)
    'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=32&p_cds=138',  # Master's in Cybersecurity
    'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=32&p_cds=136',  # Agritech Engineering
    'https://didattica.polito.it/pls/portal30/sviluppo.offerta_formativa_2019.vis?p_a_acc=2024&p_sdu=37&p_cds=30',   # Master's in Communications and Computer Networks
]

### Directory Paths
# Base directory for different data storage.
__BASE_PATH = "./TestData4"
BASE_PATH_FILE_XML = f'{__BASE_PATH}/CDL_XML_A_ACC_2024'  # Path for XML files
BASE_PATH_FILE_EXCEL = f'{__BASE_PATH}/CDL_EXCELS_A_ACC_2024'  # Path for Excel output files
BASE_PATH_FILE_RESULT_XML = f'{__BASE_PATH}/Results'  # Path for storing results
PATH_DB = "./Data/GoodDB.db"  # Database path
SEMESTRE = 1  # Choose between semester 1 or 2
