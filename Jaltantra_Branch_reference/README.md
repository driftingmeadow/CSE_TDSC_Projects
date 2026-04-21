# jaltantra

HOW TO DEPLOY THE PROJECT >>explained below>>


Jaltantra is a System for the Design and Optimization of Water Distribution Networks. 
For more info about the system, please visit the following page: 
https://www.cse.iitb.ac.in/jaltantra

This version of Jaltanra contains the user management using HttpSession. 

To work with the system, either remove/modify the @WebFilter in LoginFilter.java to bypass the login requirement 
or using MySQL, create a database named "jaltantra_db" and a table named "jaltantra_users" having the following columns:

  `id` int NOT NULL AUTO_INCREMENT,
  `fullname` varchar(100) DEFAULT NULL,
  `username` varchar(100) NOT NULL,
  `organization` varchar(150) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `country` varchar(50) DEFAULT NULL,
  `email` varchar(150) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `creationDate` datetime DEFAULT CURRENT_TIMESTAMP

You can see/modify the user credentials in the UserDao.java file. 


#temp chnage in file line 2573 
replace this 
				nodeCell = nodeRow.createCell(3);
				nodeCell.setCellValue(node.elevation);
				nodeCell.setCellStyle(doubleStyle);
      with 
        nodeCell = nodeRow.createCell(3);
        nodeCell.setCellValue(Double.parseDouble(String.format("%.2f", node.elevation)));
        nodeCell.setCellStyle(doubleStyle);

2025

Recent Updates (Jaltantra_Branch: by sakina, swapneel. )

This update introduces several improvements and configuration changes across the Jaltantra project:

	•	Build & Deployment:
	
  •	Added compile_and_deploy.sh and initialize.sh scripts for simplified setup and deployment.
	
  •	Updated .gitignore to exclude unnecessary files and binaries.
	
  •	Database & Configuration:
	
  •	Added db.sql for database initialization.
	
  •	Added google_api_key.txt for secure API key management.
	
  •	Library Updates:
	•	Replaced older mysql-connector-java-8.0.20.jar with the latest mysql-connector-j-9.4.0.jar.
	
  •	Updated OR-Tools dependency to ortools-java-9.14.6206.jar.
	
  •	Code changes:
	•	Updates in Problem.java and UserDao.java.
	•	Updated JSP files (register.jsp, system.jsp) 

Elevation Fix
1. WebContent/js/map.js
	•	Modified the getNodesJSON() function to include the elevation field when sending node data from the frontend.
	•	Ensures that elevation data (with decimals) is included in the JSON sent to the backend.

2. src/structs/MapNodeStruct.java
	•	Added a new elevation field in MapNodeStruct.
	•	Updated the constructor and toString() method to include elevation.
	•	Allows the backend to store and process node elevation data correctly.

3. OptimizerServlet.java
	•	Updated ALL occurrences of elevation formatting in Excel export.
  

Result:
	•	Elevation values are captured, stored, and exported accurately with decimals.
	•	Backend and frontend are fully synchronized for elevation data.

HOW TO DEPLOY THE PROJECT

1. Clone the Repository
2. run ./initialize.sh
3. run ./compile_and_deploy.sh