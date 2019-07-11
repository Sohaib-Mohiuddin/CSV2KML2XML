import base64
import xml.etree.ElementTree as ET
import simplekml
import tkinter 
import os
import sys
import csv
import array as arr
import IPython
import time
import logging

from PIL import Image, ImageTk
from io import StringIO
from tkinter import Label, messagebox, Button, Listbox, END, Scrollbar, Frame
from tkinter.filedialog import askopenfilename, askopenfile
from tkinter.font import Font

tk = tkinter.Tk()
tk.geometry("400x600") 
tk.title("CSV2KML2XML")
tk.resizable(False, False)
tk.configure(background = "#332f31")

thick_font1 = Font(family = "Verdana", weight = "bold", size = "25")
thick_font2 = Font(family = "Verdana", weight = "bold", size = "15")
thick_font3 = Font(family = "Verdana", weight = "bold", size = "10")

title_label = Label(tk, text = "CSV to KML to XML", height = 1, width = 18)
title_label.config(font = thick_font1, background = "#332f31", fg = "#ffffff")
title_label.pack(anchor = "center", padx = (10, 10), pady = (5, 10))

frame = Frame(tk)
frame.pack(anchor = "center", padx = "15")

message = Label(tk, text = "KML files must be located in the '/KML Files' folder", height = 1, width = 50)
message.config(font = ("Verdana", 10), background = "#332f31", fg = "#ffffff")
message.place(x = 0, y = 510)

listbox_info = Label(tk, text = "Generated KML Files are located in the", height = 1, width = 40)
listbox_info.config(font = ("Verdana", 12), background = "#332f31", fg = "#ffffff")
listbox_info.pack(anchor = "center", pady = (10, 0))
listbox_info_two = Label(tk, text = "'KML Files' Folder", height = 1, width = 35)
listbox_info_two.config(font = ("Verdana", 12), background = "#332f31", fg = "#ffffff")
listbox_info_two.pack(anchor = "center")


listbox = Listbox(frame, width = 30, height = 20, font = ("Helvetica", 12))
listbox.pack(side = "left", fill = "y")

scrollbar = Scrollbar(frame, orient = "vertical")
scrollbar.config(command = listbox.yview)
scrollbar.pack(side = "right", fill = "y")

listbox.config(yscrollcommand = scrollbar.set)

# create logger with 'spam_application'
logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('Logger.log', mode = 'w')
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

def fileConverter():
    kmlToXmlInfo()
    
    logger = logging.getLogger('KML to XML')
    
    message.config(text = "KML files must be located in the '/KML Files' folder", background = "#332f31", fg = "#ffffff")
    ftypes = [
        ('XML Document', '*.xml'), 
    ]
    try:
        inputfile = askopenfile(mode = 'rt', filetypes = ftypes)
        logger.info('Successfully opened ' + inputfile.name)
    except Exception:
        msg = messagebox.showwarning("Warning", "If 'Cancel' Button Pressed, Ignore This Message.\n\nIf File Selected, XML File May Be Corrupt. Please Select Another XML File.")
        logger.info('ERROR opening ' + inputfile.name)
        logger.info(Exception)
    tree = ET.parse(inputfile)
    root = tree.getroot()

    for case in root.findall("./ProjectSubmission"):
        caseNum = case.get('id')
        logger.info("Case Number: " + str(caseNum))

        kmldata = open("KML Files/" + caseNum + ".kml", "rb").read()
        logger.info("KML File: " + str(kmldata))

        kmlencoded = base64.b64encode(kmldata)
        logger.info("Base64 Encoded KML File: " + str(kmlencoded))

        kmldecoded = base64.decodebytes(kmlencoded)
        
        locationFileElement = case.find("LocationFile")

        if (locationFileElement.find("KLMdescription") == None):
            KLMdescriptionElement = ET.SubElement(locationFileElement, "KLMdescription")
            KLMdescriptionElement.text = "KML_" + caseNum
            KLMdescriptionElement.tail = "\n      "

            KLMSubjectElement = ET.SubElement(locationFileElement, "KLMSubject")
            KLMSubjectElement.text = "KML"
            KLMSubjectElement.tail = "\n      "

            KLMuploadtxtElement = ET.SubElement(locationFileElement, "KLMuploadtxt")
            KLMuploadtxtElement.text = str(kmlencoded)
            KLMuploadtxtElement.tail = "\n      "

            file_name_fldLocationElement = ET.SubElement(locationFileElement, "file_name_fldLocation")
            file_name_fldLocationElement.text = caseNum + ".kml"
            file_name_fldLocationElement.tail = "\n      "

            mimetypeKLMuploadElement = ET.SubElement(locationFileElement, "mimetypeKLMupload")
            mimetypeKLMuploadElement.text = "application/vnd.google-earth.kml+xml"
            mimetypeKLMuploadElement.tail = "\n      "

            isdocumentKLMuploadElement = ET.SubElement(locationFileElement, "isdocumentKLMupload") 
            isdocumentKLMuploadElement.text = "KML"
            isdocumentKLMuploadElement.tail = "\n      "
        else:
            KLMdescriptionElement = locationFileElement.find("KLMdescription")
            KLMdescriptionElement.text = "KML_" + caseNum
            KLMdescriptionElement.tail = "\n      "

            KLMSubjectElement = locationFileElement.find("KLMSubject")
            KLMSubjectElement.text = "KML"
            KLMSubjectElement.tail = "\n      "

            KLMuploadtxtElement = locationFileElement.find("KLMuploadtxt")
            KLMuploadtxtElement.text = str(kmlencoded)
            KLMuploadtxtElement.tail = "\n      "

            file_name_fldLocationElement = locationFileElement.find("file_name_fldLocation")
            file_name_fldLocationElement.text = caseNum + ".kml"
            file_name_fldLocationElement.tail = "\n      "

            mimetypeKLMuploadElement = locationFileElement.find("mimetypeKLMupload")
            mimetypeKLMuploadElement.text = "application/vnd.google-earth.kml+xml"
            mimetypeKLMuploadElement.tail = "\n      "

            isdocumentKLMuploadElement = locationFileElement.find("isdocumentKLMupload") 
            isdocumentKLMuploadElement.text = "KML"
            isdocumentKLMuploadElement.tail = "\n      "
        tree.write(inputfile.name)
        logger.info("Successfully wrote to " + str(inputfile.name)) 
    
    message.config(text = "XML File Has been Modified. Task Completed!", background = "#ffffff", fg = "#000000")
    msg = messagebox.showinfo("XML File Modified", "The KML files have successfully been added to the XML")

def askForFile():
    csvToKmlInfo()

    logger = logging.getLogger('CSV to KML')

    message.config(text = "KML files must be located in the '/KML Files' folder", background = "#332f31", fg = "#ffffff")
    listbox.delete(0, END)
    ftypes = [
        ('Microsoft Excel Comma Separated Values File', '*.csv'), 
    ]
    try:
        inputopenfile = askopenfile(mode = 'rt', filetypes = ftypes)
        logger.info('Successfully opened ' + str(inputopenfile.name))
    except Exception:
        msg = messagebox.showwarning("Warning", "If 'Cancel' Button Pressed, Ignore This Message.\n\nIf File Selected, CSV File May Be Corrupt. Please Select Another CSV File.")
        logger.info('ERROR opening ' + str(inputopenfile.name))
        logger.info(Exception)
    
    inputfile = list(csv.reader(inputopenfile))
    a = []
    dataList = []
    matchingGroup = []
    matchedGroup = []
    failedGroup = []
    prev = []
    prev = [""]*7
    last = inputfile[-1]

    if (inputfile):
        for row in inputfile[1:]: 
            if(prev[0] !=  row[0]):
                caseNum = prev[0]
                if (prev[6] == "Pass"): 
                    a += [caseNum] 
                elif (prev[6] == "Fail"):
                    a += ["Data validation failed: ..." + caseNum[-4:]]
                    failedGroup += caseNum
                    logger.info("ERROR in Generating KML for Case #: " + str(prev[0]))
                kml = simplekml.Kml()
                for data in dataList:
                    if(data[5] != "" and data[5] not in matchedGroup and data[0] not in failedGroup):
                        for row2 in dataList:
                            if(row2[5] == data[5]):
                                matchingGroup.append(row2)
                    
                        if (len(matchingGroup) > 1):    
                            first_row = matchingGroup[0]
                            second_row = matchingGroup[1]
                            line = kml.newlinestring(name = first_row[1] + "; " + second_row[1],coords = [(first_row[4],first_row[3],35),(second_row[4],second_row[3],35)])
                            line.style.linestyle.width = 5
                            line.altitudemode = simplekml.AltitudeMode.relativetoground
                            newpoint1 = kml.newpoint(name = first_row[1], description = first_row[2], coords = [(first_row[4],first_row[3])])
                            newpoint2 = kml.newpoint(name = second_row[1], description = second_row[2], coords = [(second_row[4],second_row[3])])
                            matchedGroup.append(first_row[5])
                            del matchingGroup[0:]

                    elif (data[5] == "" and data[0] not in failedGroup):
                        newpoint = kml.newpoint(name = data[1], description = data[2], coords = [(data[4],data[3])])
                        if("Outcome" not in data[1]):
                            newpoint.style.iconstyle.color = simplekml.Color.red
                        else:
                            newpoint.style.iconstyle.color = simplekml.Color.yellow

                if(prev[0] != ""):
                    if (data[6] == "Pass"):
                        try:
                            kml.save("KML Files/" + prev[0] + ".kml")
                            logger.info("Generated KML for Case #: " + str(prev[0]))
                        except Exception:
                            msg = messagebox.showerror("ERROR", "The KML For Case #: " + prev[0] + " Has Not Been Generated/Generated Correctly")
                            logger.info("ERROR in Generating KML for Case #: " + str(prev[0]))
                    del dataList[0:]

            dataList.append(row)
            prev = row

            if(prev[0] == last[0]):
                caseNum = prev[0]
                kml = simplekml.Kml()
                for data in dataList:
                    if(data[5] != "" and data[5] not in matchedGroup):
                        for row2 in dataList:
                            if(row2[5] == data[5]):
                                matchingGroup.append(row2)
                    
                        if (len(matchingGroup) > 1):    
                            first_row = matchingGroup[0]
                            second_row = matchingGroup[1]
                            kml.newlinestring(coords = [(first_row[4],first_row[3]),(second_row[4],second_row[3])])
                            matchedGroup.append(first_row[5])
                            del matchingGroup[0:]

                    elif (data[5] == ""):
                        kml.newpoint(name = data[1], description = data[2], coords = [(data[4],data[3])])

                if (data[6] == "Pass"):
                    try:
                        kml.save("KML Files/" + prev[0] + ".kml")
                        logger.info("Generated KML for Case #: " + str(prev[0]))
                    except Exception:
                        msg = messagebox.showerror("ERROR", "The KML For Case #: " + prev[0] + " Has Not Been Generated/Generated Correctly")
                        logger.info("ERROR in Generating KML for Case #: " + str(prev[0]))
                elif (data[6] == "Fail"):
                    a += ["Data validation failed: ..." + caseNum[-4:]]
                    failedGroup += caseNum
                    logger.info("ERROR in Generating KML for Case #: " + str(prev[0]))

        for item in a:
            listbox.insert(END, item) #  + ".kml"
        msg = messagebox.showinfo("Done", "Your KML Files Have Been Generated!")
    
    logger.info("Completed KML File Generation")
def csvToKmlInfo():
    msg = messagebox.showinfo("Important Information About CSV Format", "The CSV must be formatted with the following headers in order from left to right: \n" + 
        "Case Number | Name | Description | Latitude | Longitude | Group(If Necessary) | Validation \n\n" + 
        "For excel validation, the formula is: =IF(AND(41.416723<Latitude Cell, Latitude Cell <56.85012, -95.15699<Longitude, Longitutde<-71.30798),'Pass','Fail')")
def kmlToXmlInfo():
    msg = messagebox.showinfo("Important Information About XMLs and KMLs", "Please ensure the contents of <LocationFile></LocationFile> are empty. \nAlso ensure that the KML Files are stored in the 'KML Files' folder in the main directory.\n" + 
                                "The following tags will be generated in <LocationFile>:\n" + 
                                "<KLMdescription></KLMdescription>\n<KLMSubject></KLMSubject>\n<KLMuploadtxt></KLMuploadtxt>\n<file_name_fldLocation></file_name_fldLocation>\n<mimetypeKLMupload></mimetypeKLMupload>\n<isdocumentKLMupload></isdocumentKLMupload>")

kmlToXmlButton = Button(tk, text = "KML to XML", font = thick_font3, command = fileConverter, height = 2, width = 15)
kmlToXmlButton.pack(side = "right", pady = (25,10), padx = (0, 50))

csvToKmlButton = Button(tk, text = "CSV to KML", font = thick_font3, command = askForFile, height = 2, width = 15)
csvToKmlButton.pack(side = "left", pady = (25,10), padx = (50, 0))

tk.mainloop()