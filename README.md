# stackexchangeStats  

## Deletion
A simple Python application named **stackexchangeStats** that retrieves data from the StackExchange API and calculates some simple statistics.

It provides a commandline executable that takes as input a
date/time range, retrieves the StackOverflow answer data for the given time range from the StackExchange API (https://api.stackexchange.com/docs/answers) and computes the following tasks:

 - Retrieves the StackOverflow answer data for a given date/time range from the StackExchange API
(https://api.stackexchange.com/docs/answers).
 - Retrieves the comment data for a given set of answers (https://api.stackexchange.com/docs/commentsonanswers).
 - For a given date/time range calculates:
	 - the total number of accepted answers. 
	 - the average score for all the accepted answers. 
	 - the average answer count per question. 
	 - the comment count for each of the 10 answers with the highest score. 
	 - Collects and returns the calculated statistics in HTML or JSON format.

### Input example
``` 
python -m stackexchangeStats.stackexchangeStats stats --since 2016-06-02-10-00-00 --until 2016-06-02-11-00-00 --output-format json  
```  
### Output example
``` 
{
	"total_accepted_answers": 10,
	"accepted_answers_average_score": 23.8,
	"average_answers_per_question": 1.3,
	"top_ten_answers_comment_count": {
		"38149500": 1,
		"38152507": 7,
		"38147398": 5,
		"38142598": 2,
		"38149856": 0,
		"38143675": 3,
		"38143335": 1,
		"38143566": 0,
		"38143884": 9,
		"38143115": 1
	}
}
```  

## Installation  
The specific package was tested using python 2.7.15 both in Windows 10 and Ubuntu 18.10.  
  
#### Windows  
Download the file in the zip format and save it e.g. in the Downloads folder.  
Open a Command Prompt in a new folder and type:   
``` 
pip install C:\Users\user\Downloads\stackexchangeStats-1.0.zip  
```  
where in the place of the user, type your username. If you save it in another location, edit the path respectively.  
  
#### Ubuntu  
Download the file in the zip format and save it e.g. in the Downloads folder.  
Open a Terminal in a new folder and type:   
```
pip install /home/user/Downloads/stackexchangeStats-1.0.zip  
```  
where in the place of the user, type your username. If you save it in another location, edit the path respectively.  
  
## How to run the application  
  
#### Windows, Ubuntu  
Type in the same Command Prompt (Windows) or in the same Terminal (Ubuntu):  
```
python -m stackexchangeStats.stackexchangeStats stats --since 2016-06-02-10-00-00 --until 2016-06-02-11-00-00 --output-format json  
```  
  
The date\time must be in the YYYY-MM-DD-HH-MM-SS format.  
The output format can be either html or json, depending on what you type.  
The stats, --since date, --until date are required to by typed, while the --output-format and the argument after that, is optional (the default value is json), so you could also type:  
```
python -m stackexchangeStats.stackexchangeStats stats --since 2016-06-02-10-00-00 --until 2016-06-02-11-00-00  
```  
I made the hypothesis that the user will type correct date/time ranges and that there will be enough (accepted) answers, because there aren't any checks e.g. division by zero, or if the user firstly types a date that is later than the second date.
