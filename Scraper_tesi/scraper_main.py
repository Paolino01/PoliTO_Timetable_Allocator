# import scraper
# import extract_excel_from_xml
# import generateCompleteExcel
# from constantsScraper import *

# dbPath = PATH_DB

# """
#    Vengono qui generati i file xml che descrivono i corsi di laurea
# """
# scraper.__main__()
# """
#    Partendo dagli xml vengono generati i file excel (divisi per semestre) per ogni Orientamento e 
#    per ogni Corso di Laurea (Merge degli excel interni ai propri Orientamenti)
#    Gli excel a questo punto generati conterranno valori di correlazione generici:
#       0 per gli insegnamenti che non hanno problemi di sovrapposizione
#       20 per gli insegnamenti a scelta che potrebbero sovrapporsi con altri insegnamenti di qualsiasi tipo
#       90 per gli insegnamenti obbligatori ma di lingue diverse (se entrambi gli insegnamenti hanno la lingua a scelta)
#       95 per gli insegnamenti a scelta suggeriti per il corso di laura con gli insegnamenti obbligatori
#       100 per gli insegnamenti obbligatori, se entrambi obbligatori con lingua a scelta la lingua sarà la stessa
# """
# extract_excel_from_xml.__main__()
# """
#    Una volta che i file excel precedentemente generati vengono sottoposti alle modifiche dei responsabili
#    di corso bisognerà rifare il merge dei risultati, per avere un singolo file per CDL-semestre
#    In particolare serve se i docenti andranno a modificare gli excel degli orientamenti e non quelli finali
#    (percui serve rifare il merge)
# """
# extract_excel_from_xml.generateCdlExcel(menuVersion=False)
# """
#    Una volta ottenuti i file excel completi per ogni CDL (ancora con COD_INS) bisogna riunire tutte le
#    informazioni e per farlo necessitiamo di trasformare i COD_INS in id_inc.
#    La matrice finale con i soli id_inc non viene salvata in un excel ma direttamente nel db
#    Inoltre lo script prende in considerazione il file 'sovrapposizioniManuali.txt' dove andrebbero scritti
#    manualmente alcune coppie di id_inc non considerate a causa dei Moduli
# """
# if dbPath:
#    generateCompleteExcel.__main__(dbPath,1)


import scraper
import extract_excel_from_xml
import generateCompleteExcel
from constantsScraper import *

dbPath = PATH_DB

"""
   XML files describing degree programs are generated here.
   
"""
scraper.__main__()

"""
   Starting from the XML files, Excel files (divided by semester) are generated for each Specialization and
   each Degree Program (Merging Excel files within their respective Specializations).
   The Excel files generated at this stage will contain generic correlation values:
      0 for courses that do not have overlap issues
      20 for elective courses that may overlap with any other type of course
      90 for mandatory courses but in different languages (if both courses have language options)
      95 for elective courses suggested for the degree program alongside mandatory courses
      100 for mandatory courses, if both are mandatory with language options, the language will be the same
"""
extract_excel_from_xml.__main__()

"""
   Once the previously generated Excel files have been reviewed and modified by course administrators,
   the results need to be merged again to obtain a single file per CDL-semester.
   This is particularly necessary if professors modify the Excel files of the specializations and not the final ones,
   requiring a re-merging process.
"""
extract_excel_from_xml.generateCdlExcel(menuVersion=False)

"""
   Once the complete Excel files for each CDL (still with COD_INS) have been obtained, all
   information needs to be unified by transforming COD_INS into id_inc.
   The final matrix, containing only id_inc, is not saved as an Excel file but directly in the database.
   Additionally, the script takes into account the 'sovrapposizioniManuali.txt' file, where some id_inc
   pairs that were not considered due to Modules should be manually added.
"""
if dbPath:
   generateCompleteExcel.__main__(dbPath,1)
   
