# crawler_hiper
Hyper crawler challenge.

The entry point for this program is the main.py file.
It brings the data of all the products of a branch of the website: https://www.hiperlibertad.com.ar/.

The branch can be changed from the configuration file. In the event that the configuration file is deleted, it will be created when the program is executed. Working with the first branch by default.

The URLs of the branches can be obtained by manually inspecting the exchange of information between the Web browser and the Web site server at the following link: https://www.hiperlibertad.com.ar/api

The output of the crawler is a file with a csv extension that contains the data of the products of a particular branch.

Directory and file name are configurable. As well as other parameters of the .ini file.
