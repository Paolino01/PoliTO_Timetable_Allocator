# PoliTO_Timetable_Allocator

Allocator for PoliTO courses timetable

This readme was written by Paolo Cagliero.  
Email: paolocagliero2001@gmail.com  
Phone: +39 3451437020  

This file contains the documentation about the Timetable Allocator for the Politecnico di Torino. The purpose of this documentation is to provide a guide both to those who want to use the Timetable Allocator and to those who want to modify the code to add or improve constraints.  
Please note that some of the parts of the project derived from previous theses, where they were written in Italian. That's why there are some terms in Italian and some in English

The project is divided in 3 subprojects:
- Excel_to_db_converter
- Timetable_Allocator
- GUI_orario_Tesi

Besides these, there is also a folder called “Data”.

## Data
The Data folder, as the name suggests, contains the Data which the whole project relies on. We can divide the content of this folder in 2: the Database “Courses_DB.db” and the folder “Excels”.
### Database Courses_DB.db
This database, in SQLite3, contains all the data that the allocator needs to generate the timetable, as well as the results of the computation.  
There are different tables. In alphabetical order:
- Corso_di_laurea: this table contains the names of the Degree Courses for which we generate the timetable;
- Docente: the table contains the information about the names and IDs of the Teachers of all the Degree Courses we take into account;
- Docente_in_Insegnamento: this table associates each Teacher with its Teaching(s), specifying the number of hours (nOre) they have on that Teaching and the Lecture Type (tipoLez);
- Docente_in_Slot: in this table, when the timetable is generated, we save the Slots in which each Teacher has a lecture;
- Info_correlazioni: here are the correlations between Teachings. There are 2 columns, Correlazione (Correlation) and Correlazione_finale (Final Correlation). The first one represents the correlation extracted by the Scraper, the second represents the Correlation after it has been corrected by hand;
- Insegnamento: this table contains the information about each Teaching, including the Main Teacher, the hours of lecture, practice, and laboratory, the Teachers’ preferences about the allocation of those hours (n_min_double_slots, n_min_single_slots), and the information about the allocation of the Lab’s blocks (double_slots_lab = 1 if the Laboratory blocks should be of 2 Slots, 0 otherwise);
- Insegnamento_in_Orientamento: this table associates the Teachings with the Orientation(s) they belong to;
- Insegnamento_listCodIns: This table associate the IDs of the Teachings with their ID_INC (ID Incarico, different from the Teachings’ IDs because the same Teaching can have a different ID in different Orientations);
- Orientamento: this table contains the information about the Orientations of each Degree Course;
- PianoAllocazione: here is stored the list of the generated timetables. You can also provide a description for each timetable;
- PreviousSolution: this table contains a previous timetable, that can be used by CPLEX as a base to start from when generating a new timetable;
- Slot: this table contains the information about the Slots of a generated timetable. For each Teachings, we save its Slots here;
- SlotSettimana: the table saves the information about the Slots in a Week (for example, Mon. 8:30-10:00). This is used by the GUI Web Application when representing the timetable;
- Teachers_Unavailability: this table contains the Slots in which a Teacher is not available

### “Excels” folder
This folder contains the Excels files in which we can find the information about the courses. The idea is that all the information is stored in the Database, so the script “Excel_to_db_converter” reads the information from the Excel files and writes it in the Database.

In the subfolder Courses Data>Courses List we can find the file with all the information about the Teachings for the Academic Year 2025/26. This file does not only contain the Degree Courses associated to ICM and ETF colleges, but also those from other colleges. So, we have to select only the Courses we are interested in.  
The columns in which we are interested are:
- ID_COLLEGIO: contains the ID of the college (ICM or ETF);
- TIPO_LAUREA: degree type. Can be 1 (Bachelor’s Degree) or Z (Master’s Degree);
- NOME_CDL: name of the Degree Course;
- DESC_ORI: name of the Orientations in a Degree Course;
- PERIODO_INI: didactic period in which the Teaching starts (can be 1 or 2). If the Teaching can be chosen from a table, the didactic period can be found in the columns PERIODO_INI_S or PERIODO_INI_SS;
- ANNO: year of the Teaching (can be 1, 2, or 3);
- COD_INS: Teaching ID. The same Teaching can have different IDs in different Orientations;
- TITOLO: name of the Teaching. There are some Teachings (Challenge, Thesis, Internship, etc.) that we should ignore. If the Teaching can be chosen from a table by the students, in this column we will have the name of the table (for example, "Insegnamento a scelta da tabella A" and the Teaching’s name can be found in the columns TITOLO_S or TITOLO_SS);
- CFU: number of credits of the Teaching;
- ID_INC: the unique ID of the Teaching (this one does not depend on the Orientation);
- MATRICOLA: the ID of the Main Teacher for the Teaching.

The subfolder Courses Data also contains the information about the courses. Here there is one Excel file for each Degree Course.
The columns in which we are interested here are:
- h_lez: number of lecture hours of a Teaching;
- h_ese: number of practice hours and groups, in format: TYPE h_practice\*n_groups\*n_teachers  
NOTE: h_practice refers to the practice hours for each group individually;
- h_lab: number of laboratory hours and groups, in format: TYPE h_lab\*n_groups\*n_teachers  
NOTE: h_lab refers to the laboratory hours for each group individually;
- id_inc: the unique ID of the Teaching;
- matricola: ID of the Main Teacher of the Course;
- Collaboratori: this column contains the information about the collaborators of the Teaching (i.e. the Teachers other than the Main Teacher), the type of their lectures, and their hours. Refer to the Excel_to_db_converter part to understand how the column is organized and how we manage this information.

In the subfolder Teachers_Data there is the information related to the Teachers.  
Here there are the preferences of the Main Teachers about the Slot allocation of their Teachings as well as their unavailabilities. We are interested to these columns in particular:
- MATRICOLA_TITOLARE: the ID of the Main Teacher of the Teaching;
- NUM_ORE_TOT: the total number of hours of a Teaching in a semester, considering lectures, Practices, and Labs;
- NUM_ORE_ESE: the total number of Practice hours in a semester;
- NUM_SQU_ESE: number of Practice groups;
- NUM_ORE_LAB: the total number of Laboratory hours in a semester;
- NUM_SQU_LAB: number of Laboratory groups;
- ORGANIZZAZIONE_BLOCCHI_LEZIONE: contains the Teacher’s preference about the allocation of the lecture Slots. Its values can be: “tutti i blocchi da 3h” (all blocks of 3h), “un blocco da 3h e gli altri da 1,5h” (one block of 3h and the others of 1.5h), “un blocco da 4,5h (Atelier per Architettura)” (one block of 4.5h, Atelier for Architecture),;
- ORGANIZZAZIONE_BLOCCHI_ESERCITAZIONE: contains the Teacher’s preference about the allocation of the Practice Slots. Its values can be: “tutti i blocchi da 1,5h per ciascuna squadra” (all blocks of 1.5h for each group), “tutti i blocchi da 3h per ciascuna squadra” (all blocks of 3h for each group), “un blocco da 3h e gli altri da 1,5h per ciascuna squadra” (one block of 3 hours and the other of 1.5h for each group). NOTE: in some cases the Teachers request blocks of 3 hours (2 Slots), but there is only one Slot per Week. In that case we allocate blocks of 1.5 hours (1 Slot);
- NUM_BLOCCHI_SETTIMANALI_LAIB_ATENEO: number of blocks per week for the Laboratory.  
NOTE: this can be empty, but the information about the blocks per week could be found in the column NUM_BLOCCHI_SETTIMANALI_LAB_DIPARTIMENTALE
- NUM_SQUADRE_SETTIMANALI_LAIB_ATENEO: number of Lab groups.  
NOTE: this can be empty, but the information about the Lab groups could be found in the column NUM_SQUADRE_SETTIMANALI_LAB_DIPARTIMENTALE
- ORGANIZZAZIONE_BLOCCHI_LAIB_ATENEO: preference about the Slot allocation for the Lab. Its values can be: “blocchi da 1,5h per ciascuna squadra” (blocks of 1.5h for each group), “blocchi da 3h per ciascuna squadra” (blocks of 3h for each group), “indifferente” (no preference).  
NOTE: this can be empty, but the information about the organization of the Lab Slots could be found in the column ORGANIZZAZIONE_BLOCCHI_LAB_DIPARTIMENTALE;
- INDISPONIBILITA_SETTIMANALI: Slots in which the Teacher is unavailable (max. 4 per Teacher).
  
NOTE: some Teachers do not express the preferences for their Teachings here. Therefore, in order to retrieve the number of practice and laboratory hours, we have to use the columns h_ese and h_lab of the Degree Courses files.

## Excel_to_db_converter
As said before, most of the information about the Teachings and the Teachers (number of lecture, practice, and Lab hours, Teachers’ preferences about the Slot allocation, Teachers’ unavailabilities) is saved in Excel files. This Python script takes the data about Teachers and Teachings from those Excel files and saves it in the database, so that it can be used by the Allocator.

To run the program, simply execute the main.py file. It will retrieve the data from the Excel files and load it in the Database.

In the Utils folder, we have 3 files: Teaching.py, Get_Teachings_Data.py, and Get_Teachers_Data.py

### Teaching.py
This file contains a class that represents a Teaching. The information of the Teaching are retrieved from the database

### Get_Teachings_Data.py
This file contains the functions that retrieve the information about the Teachings from the Excel files and save it in the DB. We use glob and pandas to manage the Excel files from which we retrieve the information.

First of all, using the function get_teachings, we retrieve the Teachings related to te academic year 2025/26 from the file Percorsi-gruppi-insegnamenti aa 2026.xlsx and insert them into DB. We exclude those Teachings that do not require a timetable (for example, Thesis, Internship, etc.).

After doing so, we have to calculate the correlation between the Teachings. We open again the file Percorsi-gruppi-insegnamenti aa 2026.xlsx in order to retrieve the Teaching type. The correlation between two Mandatory (Obbligatori) Teachings is 100, the correlation between a Mandatory (Obbligatorio) and a Mandatory, chosen from table (Obbligatorio a scelta) Teaching is 100/n_teachings_in_table, the correlation between a Free choice (Tabella a scelta) Teaching and any other is 20, and the correlation between two Teachings of the same table (tabella a scelta) is 0. This function, after calculating the correlations, saves them in the Database.

We then load these Teachings from the DB into the list "teachings" and call the function get_teaching_information(), that gets all the files that are in the “Data/Excels/Courses Data” folder and opens them one by one. It filters the content of each file and only maintain the rows that correspond to the Teachings that are in the DB.
From those data we retrieve the ID of the Main Teacher for that Teaching and the hours of Theory Lectures for the semester. For each of those data there is a separate column in the Excels, so we directly insert them in the DB using the function db_api.add_teacher_and_lecture_hours_to_course. 

We also retrieve, using the function get_teaching_teachers, the information about collaborators of a Teaching (i.e. the Teachers other than the Main Teacher), the type of their lectures, and their hours.
This part is a bit trickier, since the information about all of the collaborators is in one column and expressed as a string. This string is in the format:
(Collaborator1 ID) NAME1 (SOMETHING) [DEPARTMENT] tit: TITLE tipo did:LECTURE_TYPE lin_LANGUAGE - h:  hh.mm; (Collaborator2 ID) NAME2 …
where [DEPARTMENT] means that the Department is optional. Be aware that there are TWO spaces between “h:” and “hh.mm”. Please also note that for some courses the same Teacher is repeated twice for the same lecture type (e.g: (ID1) NAME1 [...] tipo did:EA [...] h:  23.00; (ID1) NAME1 [...] tipo did:EA [...] h:  4.30;)

The function initially splits the string at each ; (semicolon), in order to separate the collaborators, and then, for each collaborator, separates the string using “ “ (space). Finally, we retrieve the information about the collaborator from the string and save them in the DB.
We only consider collaborators whose title is “IN” and whose lecture type is either “L” (Theory Lecture), “EA” (Practice Lecture), or “EL” (Laboratory).

### Get_Teachers_Data.py
This file contains the functions that retrieve the information about the Teachers (Slots in which they are unavailable and the preferences about the allocation of their courses).

The function get_teachers_preferences inserts in the DB the Teachers’ preferences about the allocation of the Slots of their Teachings. These preferences are in the files contained in the folder Data/Excels/Teachers Data/Teachers Preferences and are separate for Theory Lectures, Practices, and Laboratories. Be also aware that for the Laboratories the preferences can be either in the column “NUM_BLOCCHI_SETTIMANALI_LAIB_ATENEO” or “NUM_BLOCCHI_SETTIMANALI_LAB_DIPARTIMENTALE”, so we have to take this into account when reading the file.

After doing so, we call the function get_practice_lab_not_in_preferences(), which retireves from the files in the Courses Data subfolders the practice and lab hours for the Teachings that are not in the Teachers Preferences file.

For the unavailabilities, these are managed by the function get_teachers_unavailabilities. Using pandas we read the file Excel PreferenzeDocenti.xls in the Data/Excels/Teachers Data folder. We extract the slots in which a Teacher is unavailable (row["INDISPONIBILITA_SETTIMANALI"]) and insert them in the DB. Each Teacher can express a maximum of 4 unavailable Slots, so if they put more, we take into account only the first 4.



## Timetable_Allocator
Once all the data needed is retrieved by the Excel_to_DB_Converted and inserted in the Database, we can use the Timetable_Allocator project to generate a Timetable. This script models the timetable allocation problem as an Integer Linear Programming problem and uses the software CPLEX (developed by IBM) to solve it.

First of all, the script initializes the Teachings and Teachers classes, retrieving those information from the Database.

Then, by using the function get_slots_per_week(), we ask the user if they want to enable lecture allocation on Saturday and, if so, we ask them how many Slots they want to allocate on Saturday. The function returns the number of Slots in a Week, which can vary between 35 (5 Days per Week, 7 Slots per Day) and 42 (6 Days per Week, Saturday allocation enabled, 7 Slots per Day).

Then, via the function get_previous_solution, we ask the user if they want use an existing solution (which is saved in the DB in the table PreviousSolution) as a base to start from when generating the timetable. If so, we retrieve the previous solution from the DB and add it to the model.

After doing so we generate the timetable. We use an incremental approach: since generating the timetable with all the Degree Courses together would require too much time and computational power (at least two weeks with a machine with 64 threads and 100GB of RAM), we generate many timetables with a smaller set of Degree Courses each. This reduces the computational time to 4 hours and 40 minutes and also allows us to change the parameters for each subset of Degree Course. After generating a timetable, we save it in the DB and load it in the solver at the next iteration, so that the new courses are added to the ones that have already been generated.
The generation order is:
- Master's Degree of INGEGNERIA INFORMATICA (COMPUTER ENGINEERING);
- ICT FOR SMART SOCIETIES (ICT PER LA SOCIETA' DEL FUTURO), DATA SCIENCE AND ENGINEERING, ELECTRONIC AND COMMUNICATIONS ENGINEERING (INGEGNERIA ELETTRONICA E DELLE COMUNICAZIONI), COMMUNICATIONS AND COMPUTER NETWORKS ENGINEERING (INGEGNERIA TELEMATICA E DELLE COMUNICAZIONI), NANOTECHNOLOGIES FOR ICTs (NANOTECNOLOGIE PER LE ICT), INGEGNERIA DEL CINEMA E DEI MEZZI DI COMUNICAZIONE,INGEGNERIA FISICA, PHYSICS OF COMPLEX SYSTEMS (FISICA DEI SISTEMI COMPLESSI), COMMUNICATIONS ENGINEERING, QUANTUM ENGINEERING, AGRITECH ENGINEERING, CYBERSECURITY;
- ICT ENGINEERING FOR SMART SOCIETIES, INGEGNERIA DEL CINEMA E DEI MEDIA DIGITALI, CYBERSECURITY ENGINEERING, INGEGNERIA ELETTRONICA, MECHATRONIC ENGINEERING (INGEGNERIA MECCATRONICA);
- Bachelor's Degree of INGEGNERIA INFORMATICA (COMPUTER ENGINEERING);
- INGEGNERIA INFORMATICA;
- INGEGNERIA ELETTRONICA (ELECTRONIC ENGINEERING).
Changing the order of these Degree Courses can change the time needed to generate a timetable as well as the results.

We initialize the variable timetable_matrix, which will contain the timetable. Each item of timetable_matrix is identified by the tuple (teaching_id, slot_number). The item equals 1 if that Teaching has a Lecture in that slot_number, 0 otherwise.  
Practice Lectures are identified by the tuple (teaching_id_practice_groupX, slot_number). Laboratory Lectures are identified by the tuple (teaching_id_lab_groupX, slot_number).

We then add the constraints about Teachings and Teachers, using the functions add_teachings_constraints and add_teachers_constraints respectively.  
Please note that the order in which we insert the constraints matters. If you change the order, you will obtain a different solution.

### add_teachings_constraints
Here we add the constraints about the Teachings. For each constraint, we call a function that defines that constraint and adds it to the model. If we need to add the constraint for Practices and/or Laboratories as well, we call another function that adds the constraint to those kind of Lectures.  
Please refer to the Python project and to the list of constraints below to know which constraints have been implemented.

### add_teachers_constraints
Same as above, but for Teachers.  
Please refer to the Python project and to the list of constraints below to know which constraints have been implemented.

Finally, after adding all the constraints, we can solve the model by calling the function model.solve.
If a solution is found, we print it to screen and we save it in the DB, in the PianoAllocazione, Slot, and Docente_in_Slot tables. We also ask the user if they want to export the solution to an Excel file, that can be found in the Data folder. This file has one sheet for each Degree Course and in each sheet the timetables are divided by Orientation and Year.

### Parameters.py
The Allocator uses a series of parameters that can be adjusted to obtain a better timetable or to reduce the time needed to generate one. These parameters are defined in the file Parameters.py.
- slot_per_day: number of lecture Slots per Day;
- n_weeks_in_semester: number of Weeks in a Semester, used to calculate how many Slots per week need to be allocated to a Teaching;
- hours_in_slot: number of hours that are in a Slots, at the moment we have Slots of 1.5 hours;
- start_from_previous_solution: boolean variable that tells if we start from an existing solution or not;
- saturday_enabled: boolean variable that tells if we can allocate lectures on Saturday or not. Default is false;
- n_slots_saturday: saves the number of slots on Saturday. Minimum is 1, maximum is 7, default is 4;
- max_corr_in_day: number of maximum correlated Lectures in a Day;
- max_corr_first_last_slot: maximum correlation value between the first and last Slot of the Day. The lower the number, the least student will have lecture at 8:30 and 17:30 in the same Day;
- min_corr_overlaps: the minimum number of correlation between Teachings for which we guarantee that there are no overlaps;
- no_overlap_mandatory_practice_lab: if true, practices and labs of mandatory courses can not overlap with lectures of other correlated courses;
- no_overlap_groups: if true, groups of the same practice/lab can not overlap with each other;
- teachers_unavailabilities: if false, we do not consider Teachers' unavailabilities when generating the timetable;
- max_consecutive_slots_teaching: maximum number of consecutive Slots that a Teaching can have;
- teaching_overlap_penalty: the penalty in the objective function for overlaps between Teaching with a correlation < min_corr_overlaps;
- lecture_dispersion_penalty: the penalty in the objective function for lecture dispersion (defined as the difference between the first and last Lecture Slot of a Day);
- teacher_preferences_penalty: the penalty in the objective function for Teachers' preferences about Slot organization that have not been respected (note that this value should be negative, since we are trying to maximize the number of Teachers' preferences respected);
- timetable_name: the name with which the timetable is saved in the DB;
- days and time_slots: the name of the Days (“Lun”, “Mar”, “Mer”, etc.) and the Slots (“8.30-10.00”, “10.00-11.30”, etc), used when saving the timetable in the DB.


## GUI_orario_Tesi
During the previous thesis, in order to be able to visualize the timetables generated and easily read them in order to check their validity, a web application that displays the timetable via a GUI was developed. This web application reads the generated timetable in the Database and displays it in a graphical, user-friendly way.

### Allocation plan section
The web application is organized in different sections. The most important one when validating the timetables is the one related to the allocation plan. Here we can select the Allocation Plan that we are interested in validating and visualize the weekly timetable, divided by the degree type (Bachelor's or Master's Degree), the Degree Course, the Semester, and the Orientation.

### Teachers section
The Teachers section allows us to visualize the Slots for each Teacher and analyze if they have too many consecutive hours or not. You can select the allocation plan and the Teacher you are interested in and see its Teachings.

### Timetable differences section
A new section was added during this thesis: the Timetable differences section. This section is useful to compare the timetables generated with another timetable (for example, we compared our timetables with the one generated during the previous thesis related to the academic year 2023/24) in order to visualize the differences in the allocation of the single Teachings.

An analysis is provided quantifying the number of Days and Slots that have been changed from the previous timetable and how they have changed (if the Teaching's Slots have shifted towards the start or the end of the Week or if they are the same as in the other timetable).

## Constraints

The allocator implements the following constraints, divided in hard constraints (which should always be respected) and soft constraints (which should be maximized):

### Hard Constraints
#### Teachings:
- Slots per week: Each Teaching must have the exact amount of Lectures, Practices and Lab Slots per week specified in the Teaching’s description.
- Number of consecutive Slots: Each Teaching must have at most 2 Slots in a Day and, if so, the two Slots must be consecutive.
- Limited number of Teachings in a Day: The number of Correlated Teachings in a Day is limited, in order to not have too many consecutive lectures in the same Day;
- Overlaps:
  - Teachings with a Correlation above a certain threshold must never overlap. Furthermore, Mandatory Teachings must never overlap with other Teachings, regardless of their type.
  - Different Groups of Practice Lectures of the same Teaching can not overlap, since the might be only one Teacher for all the Practice Groups.
  - Same as above but for Laboratories.
  - The same groups of Practice and Laboratory Lectures of the same Teaching can not overlap (i.e. Practice Group1 of TeachingA can not overlap with Lab Group1 of TeachingA, but Practice Group1 of TeachingA CAN overlap with Lab Group2 of TeachingA only if the Practice and Laboratory Teachers are different).
  - The same Groups of Practice Lectures of different Teachings with a Correlation above a certain threshold can not overlap (i.e. Practice Group1 of TeachingA can not overlap with Practice Group1 of TeachingB, but Practice Group1 of TeachingA CAN overlap with Practice Group2 of TeachingB).
  - The same Groups of Laboratory Lectures of different Teachings with a Correlation above a certain threshold can not overlap (i.e. Lab Group1 of TeachingA can not overlap with Lab Group1 of TeachingB, but Lab Group1 of TeachingA CAN overlap with Lab Group2 of TeachingB).
- Correlation between first and last Slot of the Day: The sum of the Correlation of Teachings in the first and last Slot of the Day must be under a threshold, in order to reduce the number of Students who have lectures at 8:30 and at 17:30 in the same Day to the minimum.

#### Teachers:
- Overlaps: Teachings taught by the same Teacher must not overlap (considering Lectures, Practices, and Labs).
- Unavailable Slots: Each Teacher can indicate up to 4 Slots in which they are unavailable. Their Teachings can not be allocated in those Slots.

### Soft Constraints
- Difference between the first and last lecture of a Day: The difference between the first lecture Slot of a Day and the last one should be minimized (while maintaining some empty Slots during the Day), in order to have a more compact timetable.
- Overlaps: The overlaps between Teachings with a Correlation below the threshold should be minimized.
- Teachers’ preferences: As we said previously, the Teaching’s Main Teacher can express a preference about the Slots allocation. The amount of Slots that respect this preferences should be maximized.
