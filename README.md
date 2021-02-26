# Flask Project by G2

This project is made via Windows Subsystem for Linux. All codings are ran on Ubuntu terminal. 
We use SQLAlchemy with SQLite for our database, and this project only works on Local Server only. 

## Get started

1. Install Python 3.7 (or above)
> sudo apt-get install python3.7

2. Install PIP
> sudo apt install python3-pip

3. Update package index
> sudo apt update

4. Create and activate virtual environment
> sudo apt install python3-venv
> 
> python3 -m venv venv
> 
> source venv/bin/activate

5. Clone the repository and get into the directory
> git clone https://github.com/nurulazealia/G2_PROJECT
> 
> cd G2_PROJECT

6. Install all dependencies
> pip3 install -r requirements.txt


## Run the server

1. Open app.py file
> sudo nano app.py

2. Change the **mainpath = "/home/zh/myflaskapp/G2_PROJECT"** to your local path
```
mainpath = "insert your local path here"
```

3. Start the server locally
> python3 app.py

OR 

> python app.py


## Features available 

We provide website that allows user to record, upload, download & play audio (specially for rainsounds). 

Apart from that, our website also provides the audio reports containing the details of each audio file includes:

1. Waveform of the audio file

2. Spectogram of the audio file

3. File type

4. Audio duration

5. File size

6. Sampling frequency
 

-----------

Bisori websites has been completed.

You can watch the demo video on [Youtube](https://www.youtube.com/watch?v=U3PIj60KZuQ&feature=youtu.be).

By Aze, Ulfah and Yousouf (Members of G2)

Credit to : Asc. Prof. Muhammad Mun'im Ahmad Zabidi
