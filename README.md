# Personal Diary Application
A personal diary application is a digital tool designed to help users write and store their thoughts, reflections, emotions and important details of their lives. It is also the title of the project of Team 21. 

## Description
The app allows the user to make entries and categorize them. It offers three types of entries: A Daily Reflection, A Mood Log and An Event Note. The user can also generate a "Summary" about their activity on the app. Aside from this, the user can search files based on their name, filter files based on their type, date of creation and other properties. The user can also edit and delete existing files.

## Framework of the Backend Code
* The base class is "DiaryEntry", from which all classes inherit from.
* The main class DiaryManager includes methods like "add_entry", "search_entries", "filter_entries", and other methods for the "Summary" functionality. 
* For example: average_mood_rating: Stores the average of the mood rating present in the file 'data' into the file 'report', no_of_events: Stores the number of unique events from the file 'data' into the file 'report'
* The MoodLog class inherits from the base class, and is defined for the "Mood Log" functionality.

## Framework of the GUI
### Register and Login page
* Login button enables users to login with their credentials and also forget password if they forget it.
* Register is used to create a new user. 
* Show password shows password to confirm if user has entered desired password. 
![image](https://github.com/user-attachments/assets/d5924688-b2c5-465c-bcd9-4d962968cb82)
* If the user enters wrong password then the user gets a warning message and the login window closes

### Menu
* Displays four buttons: New entry, Search Entry, Existing entires and Summary of Diary.
* The "Back" button allows users to return to the "Personal Diary" window.

### New Entry:
Allows user to make 3 types of entries.

#### Daily Reflection
* User can enter a reflection, save and store the file using this feature. 
* All file-name have a fixed prefix "Date-DailyReflection-", after which the user can enter a name of their choice.
* Files can be bookmarked upon saving, and the list of bookmarked files can be accessed by the filter option. 
* The "Save" button allows users to save the file, with the user-given filename.
* Upon clicking Save button, the user has 10 seconds to bookmark the file ( the timer is also displayed), else the user has to go to edit entry and then bookmark it.
![image](https://github.com/user-attachments/assets/2cc9f1ed-4fab-4f87-aa33-fe048751bc42)
![image](https://github.com/user-attachments/assets/12e12a5d-83c3-40c4-bc54-573b9c509237)
* The "Back" button allows users to return to the "MENU" page.

#### Event Note
* User can make entries about the events they have attended, using the text-box to enter details like event location, attendees etc. 
* All filenames have a fixed prefix "Date-EventNote-", after which the user can enter a name of their choice.
* The "Save" button allows users to save the file, with the user-given filename.
* The "Back" button allows users to return to the "MENU" page.

#### Mood Log
* This feature allows users to make entries about their mood and emotion.
* Contains a mood log button, on clicking, we can see two options like "Mood Rating" and "Emotion tags".
* Emotion tags button contains 5 emojis which the user can choose one to reflect his emotion through out the day.
* Mood rating button provides a dropbox that lists options numbered as 1,2,3,4,5, which is the rating of the users mood. Each button generates a specific response, depending on the rating that the user has put, of their day.

### Existing Entries
* Allows users to view existing entries, as well as edit and delete them.
* Single click opens file for editing.
* Double click deletes the file.

### Search entry
* It allows user to search for a file based on the filename entered in the textbox.
* User can also filter the files based on 2 categories, Type and Date.
![image](https://github.com/user-attachments/assets/a11f33c8-9aa8-43d6-a224-dd57771db06c)
![image](https://github.com/user-attachments/assets/fb07060c-fca1-4a7b-94f5-afb3c342b62f)
![image](https://github.com/user-attachments/assets/ac997cfa-aeed-4470-986a-6003fed2e646)

### Summary of Diary
* It summarizes the users activity, such as number of events attended, trends in the mood of the user, and number of entries made, in the timeperiod chosen by the user.
* Summary is displayed using graphs and charts.
![image](https://github.com/user-attachments/assets/d6edf7a9-d445-4be4-ad24-cff54456d8d4)
![image](https://github.com/user-attachments/assets/ec9e9f6c-c62e-4224-8a48-e2b64d9a8fdc)
![image](https://github.com/user-attachments/assets/22c40485-0440-4eee-9eb5-f94de6e6cf2a)



## Getting Started
### Dependencies
* Works on Windows and Linux systems.
* Requires installation of the python libraries : Tkinter, Tkcalendar, Matplotlib. 

### Installing
* Download the zip file, and extract all files in a single folder. 
```
pip install tkinter
```
```
pip install tkcalendar
```
```
pip install matplotlib
```

### Executing program
* Open the GUI file in IDLE or VS CODE 
* Run the application using the "Run Python File" button. 

## Authors
This project has been completed with the help of: 

* BT2024229 - Akshar Singhal
* IMT20204079 - Krisha Dhokariya
* IMT2024042- Kandagatla Venkata Rohith Sai
* BT2024093 - Kalpit 
* BT2024220 -  Varun E

 ## Contributions
* Akshar: Worked largely on integrating the GUI with the backend file, and creating the basic interface of the application. Also contributed for add, edit, delete, register and login functionalities and part of bookmark functionalities, as well as the gui.
* Krisha: Made the "Daily Reflection" and "Event Note" entry functionality, along with assistance from the team. Contributed in the general gui, specifically, the theme, colours, and widget/button placements. 
* Varun: Made the "Summary of Diary" functionality. 
* Kalpit: Made search/filter functionalities. Contributed to viewing, sorting, and categorizing entries.
* Rohith: Made the "Mood Log" functionality.

## Acknowledgments
We would like to acknowledge and thank IIIT BANGLORE, Tulika ma'am and our course Teaching assistants for providing us with an opportunity to work on this project, along with giving us the required knowledge to execute it. 
