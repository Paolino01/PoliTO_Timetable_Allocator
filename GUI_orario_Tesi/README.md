# GUI_orario_Tesi
Web app that shows the generated timetable

To run the web app, open two shells in the main folder and run, in order: ./run_be.sh and ./run_fe.sh

If, when running the client, the error: "error:0308010c:digital envelope routines::unsupported" is returned, then:
- update node
- update npm
- move to the Interface folder
- run "npm uninstall react-scripts"
- run "npm install react-scripts"