#!/usr/bin/env python3

import os
import sys
import csv
import glob
import time
import serial
import qdarkstyle
import numpy as np
import subprocess as sp

from PySide2.QtWidgets import *
from PySide2 import QtGui
from PySide2 import QtCore
from image import ImageWindow, CenterPointWindow, FocusWindow

class MainWindow(QWidget):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Set a few fonts to be used
        self.small_text = QtGui.QFont()
        self.small_text.setFamily('Helvetica')
        self.small_text.setPointSize(15)

        self.large_text = QtGui.QFont()
        self.large_text.setFamily('Helvetica')
        self.large_text.setPointSize(30)

        # Group section counter
        self.section_count = 0
        self.section_start = 0
        self.started_sects = False

        # Set trackers for what sections have been taken
        self.section_a = False
        self.section_b = False
        self.section_c = False
        self.section_c = False

        # Indicator for if the image has to be taken again
        self.retake = False

        # Image counter
        self.image_count = None

        # Create the arduino connection
        # Try all three USB ports
        try:
            self.arduino = serial.Serial('/dev/ttyACM0', 9600)     #dev/cu.usbmodem14201
        except IOError:
            try:
                self.arduino = serial.Serial('/dev/cu.usbmodem14301', 9600)
            except IOError:
                try:
                    self.arduino = serial.Serial('/dev/cu.usbmodem14401', 9600)
                except IOError:
                    print("You don't have the right arduino port.")
                    sys.exit()
        # Set main window properties
        self.setGeometry(300, 300, 1200, 800)
        self.setWindowTitle('Recording Window')

        # Call the functions for initialzing the layouts
        directoryLayout = self._initDirsLayout()
        tableLayout = self._initTableLayout()
        hitLayout = self._initHitLayout()

        # Add the initialized layouts to the main layout
        mainLayout = QGridLayout()
        mainLayout.addLayout(directoryLayout, 0, 0)
        mainLayout.addLayout(tableLayout, 1, 0)
        mainLayout.addLayout(hitLayout, 2, 0)

        # Set the layout
        self.setLayout(mainLayout)

       

    def selectDirectory(self):
        '''Function for selecting an exisitng directoy'''
        return QFileDialog.getExistingDirectory(self)

    def image_dir_buttonClick(self):

        # Have the user select the directory for the images
        self.image_dir = self.selectDirectory()
        # Update the label with the directory they chose
        self.image_dir_label.setText(self.image_dir + '/')
        # Disable the button after the directory has been chosen
        self.image_dir_button.setDisabled(True)
        # Start monitoring the directoy
        # self._startWatcher()

        # Do I need to have a file list on this object?
        # if not self.backup_dir_button.isEnabled():
            # self.main_table.setDisabled(False)
            # self.hit_button.setDisabled(False)
            # self.iso_button_surface.setDisabled(False)
            # self.fstop_button_surface.setDisabled(False)
            # self.ss_button_surface.setDisabled(False)
            # msg = "<font color=green>Everything Nominal</font>"
            # self.main_label.setText(msg)
        self.backup_dir_button.setEnabled(True)
        # Populate the table
        self.populateTable()
            # self.calibrationImage()


    def backup_dir_buttonClick(self):

        # Have the user select the directory
        self.backup_dir = self.selectDirectory()
        # Update the labe with the directory they chose
        self.backup_dir_label.setText(self.backup_dir + '/')
        # Disable the button so they can't change the directory
        self.backup_dir_button.setDisabled(True)
        # Need to check that the backup directory is the same as the image directory
        self.backup()

        if not os.path.exists(self.backup_dir + '/csv_files/'):
            os.makedirs(self.backup_dir + '/csv_files/')

        # Only if both directories have been selected do we enable the rest of the GUI
        # if not self.image_dir_button.isEnabled():
        self.main_table.setDisabled(False)
        self.hit_button.setDisabled(False)
        self.iso_button_surface.setDisabled(False)
        self.fstop_button_surface.setDisabled(False)
        self.ss_button_surface.setDisabled(False)
        self.iso_button_scatter.setDisabled(False)
        self.fstop_button_scatter.setDisabled(False)
        self.ss_button_scatter.setDisabled(False)
        self.capture_button.setDisabled(False)
        self.main_button.setDisabled(False)
        temp = "<font color=green>Everything Nominal</font>"
        self.main_label.setText(temp)
            # Populate the table
            # self.populateTable()
            # self.calibrationImage()


    def backup(self):
        '''Function for backing up the image directory'''
        # Create a list of the image files is the main and backup dirs
        image_list = glob.glob(self.image_dir + '/*.nef')
        backup_list = glob.glob(self.backup_dir + '/*.nef')

        # Add the JPEGs
        image_list += glob.glob(self.image_dir + '/*.jpg')
        backup_list += glob.glob(self.backup_dir + '/*.jpg')

        # Create a list of CSV files
        csv_main_list = glob.glob(self.image_dir + '/csv_files/*')
        csv_backup_list = glob.glob(self.backup_dir + '/csv_files/*')

        # Remove any duplicates
        image_names = [x.split('/')[-1] for x in image_list]
        backup_names = [x.split('/')[-1] for x in backup_list]

        csv_main_names = [x.split('/')[-1] for x in csv_main_list]
        csv_backup_names = [x.split('/')[-1] for x in csv_backup_list]

        # Make a list of images to copy
        copy_names = [x for x in image_names if x not in backup_names]
        csv_names = [x for x in csv_main_names if x not in csv_backup_names]

        # Copy the images to the backup directoy
        for image in copy_names:
            sp.Popen(["cp", self.image_dir + '/' + image, self.backup_dir])

        for file in csv_names:
            sp.Popen(["cp", self.image_dir + '/csv_files/' +
                      file, self.backup_dir + '/csv_files/'])
        # Do we need to wait here?

    def hit_buttonClick(self):

        self.image_distance = self.image_distance + 10
        self.total_distance = self.total_distance + 10
        self.image_dist_label.setText('Image Distance: ' + str(self.image_distance) + ' um')
        self.total_dist_label.setText('Total Distance: ' + str(self.total_distance) + ' um')

        if self.image_distance == 50:
            msg = "Take An Image!"
            self.hit_button.setText(msg)
            self.hit_button.setStyleSheet("color: red")
            self.main_table.setEnabled(False)
            self.hit_button.setEnabled(False)

        # # Need to deal with what happens when 250 is hit
        # if self.total_distance % 250 == 0:
        #     msg = "<font color=red size=20>You should be taking sections</font>"
        #     self.main_label.setText(msg)
        #     # Need to make sure that the section buttons can be clicked again
        #     self.section_a = False
        #     self.section_b = False
        #     self.section_c = False
        #
        #     self.taking_sections = True

    def populateTable(self):

        # Check for CSV files
        self.csv_list = sorted(glob.glob(self.image_dir + '/csv_files/*'))

        # If the directory is empty then make a folder
        if self.csv_list == []:
            try:
                os.makedirs(self.image_dir + '/csv_files/')
            except FileExistsError:
                pass
            # Take away all of the rows
            self.main_table.setRowCount(0)
            self.main_table.setColumnCount(7)

            # initiate the table_list as empty
            self.table_list = []

        else:
            # Open the last saved csv file
            with open(self.csv_list[-1], 'r') as f:
                reader = csv.reader(f, delimiter=',')
                self.table_list = []
                for row in reader:
                    self.table_list.append(row)

            # Get the shape of the table and set the table to reflect that
            shape = np.shape(self.table_list)
            self.main_table.setRowCount(shape[0])
            self.main_table.setColumnCount(shape[1])

            # Update the total_distance
            self.total_distance = int(self.table_list[-1][1])
            self.total_dist_label.setText('Total Distance: ' + str(self.total_distance) + ' um')

            # Try and get the most recent secntion counter
            section_list = []
            total_distance = []
            for i in range(0, len(self.table_list)):
                if self.table_list[i][2] == 'None':
                    pass
                else:
                    section_list += [self.table_list[i][2]]
                    total_distance += [self.table_list[i][1]]

            if section_list == []:
                self.section_count = 0
                self.section_start = 0
            else:
                last_section_number = int(section_list[-1].split(';')[0][0])
                self.section_count = last_section_number + 1
                self.section_start = int(total_distance[0]) - 50

            # Iterate through the items in the list and set the appropriate table items
            for i, row in enumerate(self.table_list):
                for j, col in enumerate(row):
                    item = QTableWidgetItem(col)
                    self.main_table.setItem(i, j, item)

    def save(self):
        path = self.image_dir + '/csv_files/'
        # Append the image name to the csv - will make it different
        name = 'csv_depth_{0}_'.format(str(self.total_distance).zfill(4))
        name += self.table_list[-1][0][0]
        name += '.csv'

        with open(path + name, mode='w') as f:
            writer = csv.writer(f, delimiter=',')
            for row in self.table_list:
                writer.writerow(row)

        # Backup to make sure the CSV file gets copied
        self.backup()

    # Open a window for user to provide the center info of the tissure
    def centerCapture(self):
        self.setEnabled(False)
        self.center_window = CenterPointWindow(self.image_dir, self.backup_dir, self)

        self.center_window.show()
        app.processEvents()
        self.center_window.getCenter()
        self.backup()

        # wait till accept the center point.
        self.center_window.loop.exec_() 

    def imageWindowLauncher(self):

        # Need a catch in here to only call once

        self.setEnabled(False)
        self.image_window = ImageWindow(self.image_dir, self.backup_dir, self)
        self.image_window.show()
        app.processEvents()
        self.image_window.loadImage()
        self.backup()

    def _getImageName(self):

        if self.image_count == None:
            image_list = sorted(glob.glob(self.image_dir + '/*.nef'))
            if not image_list:
                self.image_count = 1
            else:
                self.image_count = int(image_list[-1].split('_')[-2])
                self.image_count += 1
        # else:
        #     #Determine what number we are on
        #     # image_list = sorted(glob.glob(self.image_dir + '/*.NEF'))
        #     self.image_count = int(image_list[-1].split('_')[-2])
        #     self.image_count += 1

        # Now create a new name
        self.surface_path = f"IMG_{self.image_count:04}_surface"
        self.scatter_path = f"IMG_{self.image_count:04}_scatter"

        self.image_count += 1

    def center_point_txt(self):
        try: 
            self.center_point_f = open(self.image_dir + '/csv_files/center_point.txt', 'r')
            self.position_list = self.center_point_f.readline().split(',')
            self.position = [np.float(self.position_list[0]), np.float(self.position_list[1])]
            self.cropped_size = [np.float(self.position_list[2]), np.float(self.position_list[3])]
            self.block_size_rescale = np.float(self.position_list[4])
        except FileNotFoundError:
            print("'center_point.txt' not exist, creating...")
            try:
                self.center_point_f = open(self.image_dir + '/csv_files/center_point.txt', 'a+')
            except FileExistsError:
                print("Fail to create {}, try to configure manually!".format(self.image_dir + '/csv_files/center_point.txt'))
                quit()

        if(int(self.scatter_path.split("_")[1]) != 1 and self.position==""):
            print("Missing center_point!")
            quit()
    


    def changeSurfaceSS(self):
        self.ss_drop_surface.setDisabled(False)

    def changedSurfaceSS(self):
        self.ss_drop_surface.setDisabled(True)

    def changeSurfaceISO(self):
        self.iso_drop_surface.setDisabled(False)

    def changedSurfaceISO(self):
        self.iso_drop_surface.setDisabled(True)

    def changeSurfaceFStop(self):
        self.fstop_drop_surface.setDisabled(False)

    def changedSurfaceFStop(self):
        self.fstop_drop_surface.setDisabled(True)

    def changeScatterSS(self):
        self.ss_drop_scatter.setDisabled(False)

    def changedScatterSS(self):
        self.ss_drop_scatter.setDisabled(True)

    def changeScatterISO(self):
        self.iso_drop_scatter.setDisabled(False)

    def changedScatterISO(self):
        self.iso_drop_scatter.setDisabled(True)

    def changeScatterFStop(self):
        self.fstop_drop_scatter.setDisabled(False)

    def save_info(self):
        try:
            camera_info = open('./camera_info.txt', 'w')
            camera_info.write(str(self.ss_drop_surface.currentText())+' ')
            camera_info.write(str(self.ss_drop_scatter.currentText())+' ')
            camera_info.write(str(self.fstop_drop_surface.currentText())+' ')
            camera_info.write(str(self.fstop_drop_scatter.currentText())+' ')
            camera_info.write(str(self.iso_drop_surface.currentText())+' ')
            camera_info.write(str(self.iso_drop_scatter.currentText()))
            # camera_info.write(str(self.block_size_drop.currentText()))

            camera_info.close()
        except FileExistsError:
            print("Fail to create 'camera_info.txt'!")


    def changedScatterFStop(self):
        self.fstop_drop_scatter.setDisabled(True)

    def _updateCapture(self):
        self.capture_button.setText("Capturing ...")
        self.capture_button.setFont(self.large_text)

    def capture_buttonClick(self):

        # Get the image names
        self._getImageName()
        self._updateCapture()

        self.center_point_txt()


        surface_iso = self.iso_drop_surface.currentIndex()
        surface_ss = self.ss_drop_surface.currentIndex()
        surface_fstop = self.fstop_drop_surface.currentIndex()

        scatter_iso = self.iso_drop_scatter.currentIndex()
        scatter_ss = self.ss_drop_scatter.currentIndex()
        scatter_fstop = self.fstop_drop_scatter.currentIndex()

        # Take the surface images
        ## Command to turn on light a
        self.arduino.write(b'a') 
        time.sleep(0.1)
        # print('image 1: ' + surface_iso)
        p = sp.Popen(["gphoto2",
                      "--set-config-index", f"iso={surface_iso}",
                      "--set-config-index", f"shutterspeed={surface_ss}",
                      "--set-config-index", f"f-number={surface_fstop}",
                      f"--filename={self.surface_path + '.%C'}",
                      "--set-config", "viewfinder=1",
                      # "--wait-event=0.5s",
                      "--capture-image-and-download"],
                      stdout=sp.PIPE, cwd=f"{self.image_dir}/")

        sout, _ = p.communicate()
        p.wait()

        self.arduino.write(b'b')
        time.sleep(0.1)
        # print('image 2: ' + scatter_iso)
        p = sp.Popen(["gphoto2",
                      "--set-config-index", f"iso={scatter_iso}",
                      "--set-config-index", f"shutterspeed={scatter_ss}",
                      "--set-config-index", f"f-number={scatter_fstop}",
                      f"--filename={self.scatter_path + '.%C'}",
                      "--set-config", "viewfinder=1",
                      # "--wait-event=0.5s",
                      "--capture-image-and-download"],
                      stdout=sp.PIPE, cwd=f"{self.image_dir}/")
        sout, _ = p.communicate()
        p.wait()

        # Turn off both lights
        self.arduino.write(b'c')
        self.capture_button.setText("Capture Image")
        self.capture_button.setFont(self.large_text)

        ######## If 1st capture, collect the center point #######
        # print(self.surface_path)
        if(int(self.scatter_path.split("_")[1]) == 1):
            self.centerCapture()

        self.center_point_f.close()

        self.imageWindowLauncher()

        self.backup()

    def main_button_clicked(self):
        self.section_a = False
        self.section_b = False
        self.section_c = False
        self.section_count += 1

    def _initTableLayout(self):
        '''Initalize the table layout'''
        # Initalize the table assuming no CSV file
        self.main_table = QTableWidget(10,7)
        self.columnLabels = ["File Name","Distance","Sections",
                             "Shutter Speed", "ISO", "Aperature", "Notes"]
        self.main_table.setHorizontalHeaderLabels(self.columnLabels)

        # Set buttons for the camera settings for the surface image
        surface_label = QLabel("Surface Image Settings")
        self.iso_button_surface = QPushButton("ISO")
        self.fstop_button_surface = QPushButton("FStop")
        self.ss_button_surface = QPushButton("SS")

        # Set buttons for the camera settings for the scatter image
        scatter_label = QLabel("Scatter Image Settings")
        self.iso_button_scatter = QPushButton("ISO")
        self.fstop_button_scatter = QPushButton("FStop")
        self.ss_button_scatter = QPushButton("SS")

        self.save_info_button = QPushButton("Save")

        # Connect the buttons for the surface image
        self.iso_button_surface.clicked.connect(self.changeSurfaceISO)
        self.fstop_button_surface.clicked.connect(self.changeSurfaceFStop)
        self.ss_button_surface.clicked.connect(self.changeSurfaceSS)

        # Connect the buttons for the scatter image
        self.iso_button_scatter.clicked.connect(self.changeScatterISO)
        self.fstop_button_scatter.clicked.connect(self.changeScatterFStop)
        self.ss_button_scatter.clicked.connect(self.changeScatterSS)
        self.save_info_button.clicked.connect(self.save_info)


        # Set the line edits for the settings
        self.ss_values = ['0.0001s', '0.0002s', '0.0003s', '0.0004s', '0.0005s', '0.0006s', '0.0008s', '0.0010s',
                          '0.0012s', '0.0015s', '0.0020s', '0.0025s', '0.0031s', '0.0040s', '0.0050s', '0.0062s',
                          '0.0080s', '0.0100s', '0.0125s', '0.0166s', '0.0200s', '0.0250s', '0.0333s', '0.0400s',
                          '0.0500s', '0.0666s', '0.0769s', '0.1000s', '0.1250s', '0.1666s', '0.2000s', '0.2500s',
                          '0.3333s', '0.4000s', '0.5000s', '0.6250s', '0.7692s', '1.0000s', '1.3000s', '1.6000s',
                          '2.0000s', '2.5000s', '3.0000s', '4.0000s', '5.0000s', '6.0000s', '8.0000s', '10.0000s',
                          '13.0000s', '15.0000s', '20.0000s', '25.0000s', '30.0000s']
        self.ss_drop_surface = QComboBox()
        self.ss_drop_surface.addItems(self.ss_values)
        # self.ss_drop_surface.setCurrentIndex(self.ss_values.index('0.0250s'))
        # self.ss_drop_surface.currentIndexChanged.connect(self.changedSurfaceSS)

        self.ss_drop_scatter = QComboBox()
        self.ss_drop_scatter.addItems(self.ss_values)
        # self.ss_drop_scatter.setCurrentIndex(self.ss_values.index('0.0031s'))
        # self.ss_drop_scatter.currentIndexChanged.connect(self.changedScatterSS)

        self.fstop_values = ['f/3', 'f/3.2', 'f/3.5', 'f/4', 'f/4.5', 'f/5', 'f/5.6', 'f/6.3', 'f/7.1', 'f/8', 'f/9',
                             'f/10', 'f/11', 'f/13', 'f/14', 'f/16', 'f/18', 'f/20', 'f/22', 'f/25', 'f/29', 'f/32']

        self.fstop_drop_surface = QComboBox()
        self.fstop_drop_surface.addItems(self.fstop_values)
        # self.fstop_drop_surface.setCurrentIndex(self.fstop_values.index('f/8'))
        # self.fstop_drop_surface.currentIndexChanged.connect(self.changedSurfaceFStop)

        self.fstop_drop_scatter = QComboBox()
        self.fstop_drop_scatter.addItems(self.fstop_values)
        # self.fstop_drop_scatter.setCurrentIndex(self.fstop_values.index('f/8'))
        # self.fstop_drop_scatter.currentIndexChanged.connect(self.changedScatterFStop)

        self.iso_values = ['100', '125', '160', '200', '250', '320', '400', '500', '640', '800', '1000', '1250', 
        				   '1600', '2000', '2500', '3200', '4000', '5000', '6400', '8000', '10000', '12800', '25600']

        self.iso_drop_surface = QComboBox()
        self.iso_drop_surface.addItems(self.iso_values)
        # self.iso_drop_surface.setCurrentIndex(self.iso_values.index('100'))
        # self.iso_drop_surface.currentIndexChanged.connect(self.changedSurfaceISO)

        self.iso_drop_scatter = QComboBox()
        self.iso_drop_scatter.addItems(self.iso_values)
        # self.iso_drop_scatter.setCurrentIndex(self.iso_values.index('100'))
        # self.iso_drop_scatter.currentIndexChanged.connect(self.changedScatterISO)
       

        # Getting previous saved camera info
        # ss_value_surface ss_value_scatter fstop_value_surface fstop_value_scatter iso_value_surface iso_value_scatter
        try: 
            camera_info = open('./camera_info.txt', 'r')
            camera_info_list = camera_info.readline().split(' ')
           
            self.ss_drop_surface.setCurrentIndex(self.ss_values.index(camera_info_list[0]))
            self.ss_drop_surface.currentIndexChanged.connect(self.changedSurfaceSS)

            self.ss_drop_scatter.setCurrentIndex(self.ss_values.index(camera_info_list[1]))
            self.ss_drop_scatter.currentIndexChanged.connect(self.changedScatterSS)

            self.fstop_drop_surface.setCurrentIndex(self.fstop_values.index(camera_info_list[2]))
            self.fstop_drop_surface.currentIndexChanged.connect(self.changedSurfaceFStop)

            self.fstop_drop_scatter.setCurrentIndex(self.fstop_values.index(camera_info_list[3]))
            self.fstop_drop_scatter.currentIndexChanged.connect(self.changedScatterFStop)

            self.iso_drop_surface.setCurrentIndex(self.iso_values.index(camera_info_list[4]))
            self.iso_drop_surface.currentIndexChanged.connect(self.changedSurfaceISO)

            self.iso_drop_scatter.setCurrentIndex(self.iso_values.index(camera_info_list[5]))
            self.iso_drop_scatter.currentIndexChanged.connect(self.changedScatterISO)

            camera_info.close()

        except FileNotFoundError:
            print("'camera_info.txt' not exist, using default value...")
            self.ss_drop_surface.setCurrentIndex(self.ss_values.index('0.0250s'))
            self.ss_drop_surface.currentIndexChanged.connect(self.changedSurfaceSS)

            self.ss_drop_scatter.setCurrentIndex(self.ss_values.index('0.0031s'))
            self.ss_drop_scatter.currentIndexChanged.connect(self.changedScatterSS)

            self.fstop_drop_surface.setCurrentIndex(self.fstop_values.index('f/8'))
            self.fstop_drop_surface.currentIndexChanged.connect(self.changedSurfaceFStop)

            self.fstop_drop_scatter.setCurrentIndex(self.fstop_values.index('f/8'))
            self.fstop_drop_scatter.currentIndexChanged.connect(self.changedScatterFStop)

            self.iso_drop_surface.setCurrentIndex(self.iso_values.index('100'))
            self.iso_drop_surface.currentIndexChanged.connect(self.changedSurfaceISO)

            self.iso_drop_scatter.setCurrentIndex(self.iso_values.index('100'))
            self.iso_drop_scatter.currentIndexChanged.connect(self.changedScatterISO)

        # Set the font for the buttons
        self.iso_button_surface.setFont(self.small_text)
        self.fstop_button_surface.setFont(self.small_text)
        self.ss_button_surface.setFont(self.small_text)

        self.iso_button_scatter.setFont(self.small_text)
        self.fstop_button_scatter.setFont(self.small_text)
        self.ss_button_scatter.setFont(self.small_text)

        # Initally disable the table until the directories have been chosen
        self.main_table.setDisabled(True)
        self.iso_button_surface.setDisabled(True)
        self.fstop_button_surface.setDisabled(True)
        self.ss_button_surface.setDisabled(True)

        self.iso_button_scatter.setDisabled(True)
        self.fstop_button_scatter.setDisabled(True)
        self.ss_button_scatter.setDisabled(True)

        # make the table expand over the button
        self.main_table.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding)

        # Center the lables
        scatter_label.setAlignment(QtCore.Qt.AlignCenter)
        surface_label.setAlignment(QtCore.Qt.AlignCenter)

        self.iso_drop_surface.setDisabled(True)
        self.fstop_drop_surface.setDisabled(True)
        self.ss_drop_surface.setDisabled(True)

        self.iso_drop_scatter.setDisabled(True)
        self.fstop_drop_scatter.setDisabled(True)
        self.ss_drop_scatter.setDisabled(True)

        header = self.main_table.horizontalHeader()

        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.Stretch)
        # header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        settings_layout = QGridLayout()
        settings_layout.addWidget(surface_label, 0, 0, 1, 2)
        settings_layout.addWidget(self.iso_button_surface, 1, 0)
        settings_layout.addWidget(self.fstop_button_surface, 2, 0)
        settings_layout.addWidget(self.ss_button_surface, 3, 0)
        settings_layout.addWidget(self.iso_drop_surface, 1, 1)
        settings_layout.addWidget(self.fstop_drop_surface, 2, 1)
        settings_layout.addWidget(self.ss_drop_surface, 3, 1)
        settings_layout.addWidget(scatter_label, 4, 0, 1, 2)
        settings_layout.addWidget(self.iso_button_scatter, 5, 0)
        settings_layout.addWidget(self.fstop_button_scatter, 6, 0)
        settings_layout.addWidget(self.ss_button_scatter, 7, 0)
        settings_layout.addWidget(self.iso_drop_scatter, 5, 1)
        settings_layout.addWidget(self.fstop_drop_scatter, 6, 1)
        settings_layout.addWidget(self.ss_drop_scatter, 7, 1)
        settings_layout.addWidget(self.save_info_button, 8, 0, 2, 1)
        settings_layout.setColumnStretch(0, 10)
        settings_layout.setColumnStretch(1, 30)
        # settings_layout.setColumnStretch(2, 10)

        # settings_layout.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        # Make the talbe have its own layout
        # Not sure this is necessary as the table isn't that complicated
        layout = QGridLayout()
        layout.addWidget(self.main_table, 0, 0)
        layout.addLayout(settings_layout, 0, 1)
        layout.setColumnStretch(0, 50)
        layout.setColumnStretch(1, 10)

        return layout

    def _initDirsLayout(self):

        # Add the directory buttons
        self.image_dir_button =  QPushButton("Select Image Folder")
        self.backup_dir_button =  QPushButton("Select Backup Folder")
        self.capture_button = QPushButton("Capture Images")

        # Add the directory labels
        self.image_dir_label = QLabel()
        self.backup_dir_label = QLabel()
        self.image_dist_label = QLabel()
        self.main_label = QLabel()
        self.main_button = QPushButton("Reset Sections")

        # Change the font of all the lables and buttons
        self.image_dir_label.setFont(self.small_text)
        self.backup_dir_label.setFont(self.small_text)
        self.image_dist_label.setFont(self.small_text)
        self.main_label.setFont(self.small_text)
        self.main_button.setFont(self.small_text)
        self.image_dir_button.setFont(self.small_text)
        self.backup_dir_button.setFont(self.small_text)
        self.capture_button.setFont(self.large_text)

        # Set the size policy for the label so it expands vertically
        self.main_label.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding)
        self.main_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.capture_button.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)

        # Initalize the messages for the main label and the directories
        msg = "<font color=red>Please select the Image and Backup Directories</font>"
        self.image_dir = "/Path/to/image/directoy/"
        self.backup_dir = "/Path/to/backup/directoy/"
        self.main_message = msg

        # Set the labels with the inital messages
        self.image_dir_label.setText(self.image_dir)
        self.backup_dir_label.setText(self.backup_dir)
        self.main_label.setText(self.main_message)

        # Set the alignment of the main text
        self.main_label.setAlignment(QtCore.Qt.AlignCenter)
        self.main_label.setFont(self.large_text)

        # Connect the buttons to their functions
        self.image_dir_button.clicked.connect(self.image_dir_buttonClick)
        self.backup_dir_button.clicked.connect(self.backup_dir_buttonClick)
        self.capture_button.clicked.connect(self.capture_buttonClick)
        self.main_button.clicked.connect(self.main_button_clicked)

        # Diable the backup directory button at first
        self.backup_dir_button.setEnabled(False)
        self.capture_button.setEnabled(False)
        self.main_button.setDisabled(True)

        # Define the layout for the main window
        layout = QGridLayout()
        layout.setColumnStretch(0, 0)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        layout.addWidget(self.image_dir_button, 0, 0)
        layout.addWidget(self.image_dir_label, 0, 1)
        layout.addWidget(self.backup_dir_button, 1, 0)
        layout.addWidget(self.backup_dir_label, 1, 1)
        layout.addWidget(self.capture_button, 0, 2, 2, 1)
        layout.addWidget(self.main_label, 2, 1, 1, 2)
        layout.addWidget(self.main_button, 2, 0, 1, 1)

        return layout

    def _initHitLayout(self):

        # Make the hit button and the lables for the section distances
        self.hit_button = QPushButton("HIT!!!")
        self.image_dist_label = QLabel()
        self.total_dist_label = QLabel()

        # Set the font for the labels and button
        self.image_dist_label.setFont(self.large_text)
        self.total_dist_label.setFont(self.large_text)
        self.hit_button.setFont(self.large_text)

        # Set the size policies for the buttons and labels
        self.hit_button.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding)
        self.image_dist_label.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding)
        self.total_dist_label.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding)

        # Initalize the distances
        self.image_distance = 0
        self.total_distance = 0

        # Make the labels for the distances
        # Keep the number separate from the text so they can easily be used elsewhere
        self.image_dist_label.setText('Image Distance : ' + str(self.image_distance) + ' um')
        self.total_dist_label.setText('Total Distance : ' + str(self.total_distance) + ' um')

        # Connect the hit button
        self.hit_button.clicked.connect(self.hit_buttonClick)

        # Disable the hit button initally
        self.hit_button.setDisabled(True)

        # Create the layout
        layout = QGridLayout()
        layout.addWidget(self.hit_button, 0, 0, 2, 1)
        layout.addWidget(self.image_dist_label, 0, 1)
        layout.addWidget(self.total_dist_label, 1, 1)
        layout.setColumnStretch(0, 20)
        layout.setColumnStretch(1, 15)

        return layout

    def errorMessage(self, error):
       msg = QMessageBox()
       msg.setIcon(QMessageBox.Critical)
       msg.setText(error)
       # msg.setInformativeText("This is additional information")
       msg.setWindowTitle("ERROR")
       # msg.setDetailedText("The details are as follows:")
       msg.setStandardButtons(QMessageBox.Ok)
       # msg.buttonClicked.connect(msgbtn)

       msg.exec_()
       # print "value of pressed message box button:", retval


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
     
    window = MainWindow()

    window.show()

    # Focus here
    focus_window = FocusWindow()
    focus_window.show()

    app.exec_()
    # window.watcher.stop()
    # window.thread.quit()
    # window.thread.wait()
