# Q-A

## Brief
The overall objective of this project is to create a CRUD application with utilisation of supporting tools, methodologies and technologies that encapsulate all core modules covered during training.

## User Stories
- [x] Users are able to create an account
- [x] Users are able to ask a question
- [x] Users are able to answer a question
- [x] Users are able to edit their question
- [x] Users are able to delete their question

## Tasks
- [x] Allow the user to CREATE an account
- [x] Allow the user to CREATE a question
- [x] Allow the user to CREATE an answer
- [x] Allow the users to READ previously made questions and answers
- [x] Allow the users to UPDATE a question
- [x] Allow the user to DELETE a question and its answers

## CI Pipeline
Project Tracking: Jira \
VCS: Git \
Source Code: Python \
Database: GCP SQL Server \
Cloud server: GCP Compute Engine \
Front-end: Flask \
Unit Testing: Pytest \
Integration Testing: Selenium \
CI Server: Jenkins

## Project Tracking
![jiraboard1](https://user-images.githubusercontent.com/66832040/89731199-06ca4180-da3d-11ea-8346-753f2619698e.png) \
This is my Jira board at the begining of my project. I feel that this application checks all of the user stories and tasks that were listed above and within the Jira board.

## ERD
![ERD](https://user-images.githubusercontent.com/66832040/89564451-f0da3800-d814-11ea-8e01-68862dac9a07.png) \
When creating the ERD, I had first decided to only do two tables, one for the users and the other for the questions and answers. After thinking about it for awhile, I decided that it would make more sense to do three tables, one for users, one for the questions and one for the answers. Using this ERD makes it easier for the users to be able to see who wrote a question, and who answered it. It also makes it easier to store this information in the tables as it just means that one table isn't going to be constantly changed.

## Testing
![testing](https://user-images.githubusercontent.com/66832040/89731058-067d7680-da3c-11ea-9af1-ec2f90b86d5f.png) \
Pytest and Selenium have been used for automated testing. I was able to get a coverage of 94%. Within the tests, I covered all the main functionalities of this application and found no issues with the code. I believe that a higher coverage score could have been reached if there was more Selenium tests completed.

## Risk Management
![risk](https://user-images.githubusercontent.com/66832040/89736838-5839f700-da64-11ea-995d-990b4aca8f1d.png)

## Future Improvements
For future improvements, I think it would be great if the answers to the questions were shown below them instead of them all being shown on a seperate page. I also think there should be a page to allow users to update their information such as their usernames and passwords
