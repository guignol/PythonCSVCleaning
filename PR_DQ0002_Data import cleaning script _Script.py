# -*-coding:utf-8 -*
#-----Importing modules needed in the programm
#os module is used to dialog with the native operation system
#subprocess module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes
#csv module is used to treat easely csv files
#re module is used to treat regular expressions
#codec module is used to treat file encoding
import os, subprocess, csv, re, codecs

#fnmatch module is a shortcut for findmatch is like ctrl+f for the program
from fnmatch import fnmatch

#mkstemp module is used for temp file treatment
from tempfile import mkstemp
#move module allows the program to move file
from shutil import move

#remove and close modules are used to treat with file management
from os import remove, close



#------Definition of the different function the script will be using
def replace(source_path, out_path, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    	
    old_file = open(source_path,encoding="utf-8-sig")
    new_file = open(abs_path,'w',encoding="utf8")
    for line in old_file:
        new_file.write(line.replace(pattern, subst))
    #close temp file
    new_file.close()
    close(fh)
    old_file.close()
    #Remove original file id needed
    #remove(source_path)
    #Move new file
    move(abs_path, out_path)

def cleancsv(source_path):
    #Create temp file
    fh, abs_path = mkstemp()
    new_file = open(abs_path,'w',encoding="utf-8-sig")
    old_file = open(source_path,encoding="utf8")

    for line in old_file:
        new_file.write(re.sub(regexp, '',line))
    #close temp file
    new_file.close()
    close(fh)
    old_file.close()
    #Remove original file id needed
    #remove(source_path)
    #Move new file
    move(abs_path, source_path)

def addsource(source_path,source_name):
    #--Initiate variables
    #Create temp file
    fh, abs_path = mkstemp()

    #--Open files
    #open the temp file as a utf-8-sig encoding (utf-8 with no BOM)
    new_file = open(abs_path,'w',encoding="utf-8-sig")
    #open the temp file as a utf-8
    old_file = open(source_path,encoding="utf8")


    #--Write files
    #copy each lines (line) from the previous file (old_file) to the new one (new_file)
    for line in old_file:
        new_file.write(line)


    #--Close files
    #close new file
    new_file.close()
    #close temp file
    close(fh)
    #close old file
    old_file.close()

    #Move new_file previously stored in the abs_path variable to the source_path to replace the old_file 
    move(abs_path, source_path)





#------Starting the program-----
#--Initiate variables
#input path for incoming data be careful to use double backslash as a directory separator
inputdir = 'C:\\Input'
#input path for outcoming data be careful to use double backslash as a directory separator
outputdir = 'C:\\Output'
# defining the regular expression to delete the expression "(X row(s) affected)" inserted in the query export (where X is the number of records in the csv file)
#the equivalent regular expression of the "(X row(s) affected)" is ^\(\d+ row\(s\) affected\)$
regexp = '^\(\d+ row\(s\) affected\)$'
#file filter for file selection in folder and subfolder of the input directory (inputdir)
filepattern = '*.csv'

#regexpforquotes='^"d+'

#-----Running conversion------
#--for each path, subdirectory and files under the input directory is made using the os.walk function imported with the os module
#--path looks like "C:\folder\"
#--files looks like [file1.csv,file2.csv,file3.csv]
for path, subdirs, files in os.walk(inputdir):
    #--for each file (the title is catch as "name" variable) in the current browsed directory file list (files)
	#--name looks like "file1.csv"
    for name in files:
        #--if the filename (name) match the filepattern (that is to say if  it's a .csv file) execute file treatment
		if fnmatch(name, filepattern):
            #Source of the file joining the full path file name "c:\folder\file.csv"
			source = os.path.join(path, name)
            #print the user a log line displaying the current processed file "c:\folder\file.csv"
            print ('converting :' + source)
			destination = outputdir + '\\' + name
            #replacing the ; with _ to be sure that ; won't be considered as a column separator anymore
            #source is the "source" file to be treated and "destination" is the source file treated 
            #this action is the equivalent of copy+paste+replacing on the paste file
			replace(source,destination,";","_")
            #replacing the separator of treated file with a standard column separator
			replace(destination,destination,"~",";")
            #replacing "zero date" by null value
			replace(destination,destination,"1900-01-01 00:00:00.000","")
			#truncating date/time format for a date format only
            replace(destination,destination,"00:00:00.000","")
            #cleaning the csv file by deleting the query report at the end of the file i.e. "(X row(s) affected)" expression
			cleancsv(destination)
            #
			addsource(destination,name)


os.system("pause")

