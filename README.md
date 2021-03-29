# DriveSorter
A program that sorts your google drive using AI

# Problem
The problem that this project solves is students in distance learning having a disorganized didgital workspace. This project uses Word2Vec, the Google Drive API, and Python to sort the user's files into folders that represent the classes, clubs, and activity that that student is engaged in.

# Installation
Use the following pip commands to install the required libraries:
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip install numpy
pip install gensim
pip install --upgrade httplib2
(Note: if gensim isn't properly installing, try using pip unistall numpy and then pip install numpy).

# How to run the project
Download the repo and download the pretrained model. Follow the instructions at this link https://developers.google.com/drive/api/v3/quickstart/python to enable the API. Pick Desktop App. After enabling the API, you should then be able to download a 'credentials.json' file. Put this in your project. Then run 'quickstart.py'. The first time you run it it will print a link and ask you to authenticate your google account. After you do this and give the program permission to access your Google Drive, the program will then sort your files. It will print out each file name with the folder that it is assigned to. You may notice that the program takes a while (about a minute) before asking for authentication and running. This is because the program needs to load the pretrained model, which may take a bit of time.

# How it works
Our code first access the user's Google Drive using Google Drive API v3. When the user first uses it they have to undergo and authentication process, but afterwords they don't need to authenticate themselves. To force the program to reauthenticate the user, delete the 'token.json' file. Our code then creates four folders in the user's Google Drive; Math, Science, Language Arts, and English. The 'subjects' array can also be modified to include more folders. If those folders were already created by the program in a previous run, the IDs for them would have been stored in requirements.txt and the program will instead access the ids from requirements.txt. (Note: before the program is first run, requirements.txt should be blank and if you delete the folders from your drive, requirements.txt should be made blank again). The program then loops over all of the user's files and uses the AI sorting system (more information reguarding that below) to find the folder that the file name is closest to. A shortcut to that file is then created in that folder. This is done in the quickstart.py file, and the AI sorting system is made in the sort.py file.

# How the AI sorting system works
Our AI sorting system (which is made in the sort.py file) finds which folder the file would fall into based on that file's name (for example, a file named Polynomials Test would go into the math folder). The program uses Word2Vec and a pretrained Word2Vec model to get the vector representation of the words. The vector representations of the words represent the meaning of the word and how it relates to other words (for example, if you get the vector for king and subtracted the vector for man and then added the vector for women, you may get the vector of queen as the output). Our program first gets the vector of the folder and then, for each word in the file name, gets the similarity of that word to the folder. The similarity of each word to the folder is than averaged. Words that can't be converted into vectors or are commonw words aren't considered. The program is able to tell if two vectors are similar by using the equation (A*B)/(||A||*||B||), where A and B are vectors, A*B is the dot product of A and B, ||A|| is the magnitude of A, and ||B|| is the magnitude of B.
