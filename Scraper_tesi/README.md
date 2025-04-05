# Scraper_Tesi

## scraper.py:
  Script that generates all the XML files for the various degree programs (CDL).
  It is necessary to first define the URLs in the `constantScraper.py` file. In the same file, you can define the folder names where the Excel and XML files will be stored.
  (Some functions and data structures necessary for the scraper's operation are within `auxScraper.py`.)
  
## extract_excel_from_xml.py
  Script that reads the XML files and generates Excel matrices by placing correlation values between various pairs of courses.
  
  #### Folder structure of the Excel files:
    
    [CDL_EXCELS] (Arbitrary folder name, root):  # Items in brackets are directories, * denotes repeating elements
      *[CDL_NAME]:
        *[SPECIALIZATION_NAME]:
          excel_specialization_semester1.xlsx
          excel_specialization_semester2.xlsx
       excel_cdl_semester1.xlsx
       excel_cdl_semester2.xlsx

    [CDL_EXCELS](Nome cartella arbitrario, root):  # Tra [] le directory, * elementi che si ripetono
      *[NOME_CDL]:
        *[NOME_ORIENTAMENTO]:
          excel_orientamento_semestre1_xlsx
          excel_orientamento_semestre2.xlsx
       excel_cdl_semestre1.xlsx
       excel_cdl_semestre2.xlsx

       
       
   #### Categorization of courses:
    A - Mandatory course: Available in only one language.
    B - Mandatory elective course: Available in both English and Italian.
    C - Elective course: A course from a table (Courses in the table differ from each other).
   
   #### Semantics of correlation values in the Excel files:
    - 100: Mandatory courses must not overlap (Hard constraint).
    - 95: Recommended courses have a high value with mandatory courses to try to prevent overlap.
    - 90: If a course is chosen in a different language than the main program, an effort is made to avoid overlap but without strictly enforcing it.
    - 20: Symbolic value, meaning that there is an instance where the two considered courses can be chosen by a student for the same academic period.
    - 0: There is no instance where the two courses can be chosen by a student for the same academic period.

## generateCompleteExcel.py
  Script that, starting from the `excel_cdl_semesterX.xlsx` files of all degree programs and using data from the database, transforms pairs formed by course codes into pairs of `ID_INC` so that a globally valid value can be found regardless of the degree program under examination.
  
  If you want to use this script, you need to manually specify the database name inside `main.py`.

## main.py
  Execution of the scripts described above.

