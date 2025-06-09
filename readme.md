#_author_: Nafiz Farhan Bin Zainurin
#_project_: Masterthesis with the title "Design of Modular Model Predictive Control for Building Automation"

To run the project, run "gui_main.py"

gui_main.py 				- This is the main file (Main GUI). Running this file will run the whole program
gui_sub						- This is second GUI. Can be run on its own to see the GUI and test its functionality
controller.py 				- This is the MPC program. Can be run on its own to compute MPC but make sure database contain enough data, otherwise run it from gui_main.py
progressBar.py 				- This the basic custom made progress bar. Can be run on its own to see how it works. For test purpose, it uses timer to simulate MPC computation.
primaryWindow_ui_6.py 		- This is the gui file for the primary window. Developer can check the name of the widget correspond to which widget. This is only for reference. 
							- Called by gui_main.py
secondWindow_ui_8.py 		- This is the gui file for the secondary window. Developer can check the name of the widget correspond to which widget. This is only for reference.
							- Called by gui_sub.py

uploadData_yearly_15minute.py - This is the file that upload and read the data. Uploading data is done manually in this file. And the interval is fix for 15 minutes and cannot be changed.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

controller.py
-------------
For the controller, the configuration are not adapted to other parameter such as:
	
	-Prediction horizon	: Currently is set to 24 hours correspond to 96 step when sampling time is 15 minutes.
	-control horizon	: Currently set to 1, but changing it to other number will require an adaptation in function "shift_timestep(t,x,u,h)". So now it is fix to 1
	-sampling time 		: When this is changed, the interval of the uploaded data also need to be changed. At the moment, the sampling time is fixed to 15 minutes.
	-Duration of Sim.	: The current data only contain information for 6 days, therefore value cannot be more that 6.
	-Room Temperature	: Parameter is not used and this parameter can be used for future improvement.
	-Range of tol. 		: Parameter is not used and this parameter can be used for future improvement.

When executed, a progress bar will pop up and inform the user how many percent the computation already completed. 

The functionality of the progress bar itself is alright as was tested in the "progressBar.py" (Run the program "progressBar.py") but when integrated with the "controller.py", it is quite buggy.
The program will freeze when the user click the progress bar window. DO NOT CLICK ON THE PROGRESS BAR WINDOW. because it will freeze and it will show "window is not responding..". But after another 
iteration is completed, it will be alright again.
	

gui_sub.py
----------
Overview tab 	: -The "utilities" group box are disabled since enabling/disabling the checkbox require the "Heat Pump", "Battery" and "Electric Vehicle" tab to adapt to the checkbox appear/disappear. 
				   This functionality can be extended for future work.
				  - Availability of heat pump: Always yes
				  - Number of batteries: depends on the row of the table in the "Battery" tab
				  - Number of electric vehicles: depend on the row of the table in the "Electric Vehicle" tab
Heat Pump		: - They are first initialize with a default value. User can change this value and save it. Rerunning the program will load the last save value. 
				  - When saving to database is succesfull, a pop-up window will appear.
Solar Panel		: - They are first initialize with a default value. User can change this value and save it. Rerunning the program will load the last save value
				  - When saving to database is succesfull, a pop-up window will appear.
Controller		: - They are first initialize with a default value. User can change this value and save it. Rerunning the program will load the last save value
				  - When saving to database is succesfull, a pop-up window will appear.
				: - The modes are associated with a certain value for enumeration purpose(except "Advance Setting...")
				 		# Default Model		: 1
				 		# Energy Saving Mode: 2
				 		# Economic Model	: 3
