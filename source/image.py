import numpy as np

from PySide2.QtWidgets import *
from PySide2 import QtGui
from PySide2 import QtCore
# from rawkit.raw import Raw
import imageio, pyexiv2
import os, psutil
# from unet import predict
# from unet.unet import UNet
import cv2
from PIL import Image
from IterativeSegmentationAdaptive import segmenation_LDA

import gphoto2 as gp
from skimage.transform import rescale
from SegmentNNGui import *

import subprocess as sp
import qimage2ndarray
import rawpy, time, skimage

import concurrent.futures


# class FocusWindow(QWidget):
#     def __init__(self, main, parent=None):
#         super(FocusWindow, self).__init__(parent)

#         # Set main window properties
#         self.setGeometry(250, 250, 1400, 700)
#         self.setWindowTitle('Center Point Window')

#         self.main_window = main
        
#         self.timer = QtCore.QTimer(self)

#         self.timer.timeout.connect(self.displayFrame)

#         self.setLayout(self.initLayout())


#     #     super().__init__()
#     #     self.title = 'PyQt5 Video'
#     #     self.left = 100
#     #     self.top = 100
#     #     self.width = 640
#     #     self.height = 480
#     #     self.initUI()

#     # # @QtCore.Qt.pyqtSlot(QImage)
#     # def setImage(self, image):
#     #     self.label.setPixmap(QPixmap.fromImage(image))

#     # def initUI(self):
#     #     self.setWindowTitle(self.title)
#     #     self.setGeometry(self.left, self.top, self.width, self.height)
#     #     self.resize(1800, 1200)
#     #     # create a label
#     #     self.label = QLabel(self)
#     #     self.label.move(280, 120)
#     #     self.label.resize(640, 480)
#     #     th = Thread(self)
#     #     th.changePixmap.connect(self.setImage)
#     #     th.start()
#     #     self.show()
#     #     super(FocusWindow, self).__init__(parent)

#     #     # Set main window properties
#     #     self.setGeometry(200, 200, 1350, 1200)
#     #     self.setWindowTitle('Focus Window')

#     #     # self.main_window = main
#     #     self.setLayout(self.initLayout())
        

#     def displayFrame(self):
#         cap = cv2.VideoCapture(0)

#         cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1250)
#         cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1000)
#         ret, frame = cap.read()
#         if(ret):
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             image = qimage2ndarray.array2qimage(frame)
#             pixmap = QtGui.QPixmap.fromImage(image)
#             resizeImage = pixmap.scaled(1250, 1000, QtCore.Qt.KeepAspectRatio)
#             self.label.setPixmap(resizeImage)

#     def stop(self):
#         self.timer.stop()

#         # self.p.kill()
#         # self.p.terminate()

#         # self.arduino.write(b'c')
#         pid = os.getpid()
#         parent = psutil.Process(pid)

#         # except psutil.Error:
#         #     # could not find parent process id
#         #     return

#         for child in parent.children(recursive=True):
#             child.terminate()
#         # self.p.wait()
#         # print(self.p.pid)
#         # os.kill((self.p.pid), signal.SIGTERM)

#         self.close()
#         self.destroy()


#     def initLayout(self):
#           # OPENCV
#         self.label = QLabel('No Camera Feed')
#         button = QPushButton("Quiter")
#         button.clicked.connect(self.stop)

#         layout = QVBoxLayout()
#         layout.addWidget(button)
#         layout.addWidget(self.label)
#         self.setLayout(layout)
#         self.timer.start(60)

#         # self.arduino.write(b'b')
#         self.p = sp.Popen(["/home2/tester/Desktop/recordingGui-master/focus.sh"], shell=True, stdout=sp.PIPE)
#         # sout, _ = self.p.communicate()
#         # self.p.wait()
#         # self.p.kill()

#         # os.killpg(os.getpid(), signal.SIGTERM)
#         # print(os.getpid())
#         # p = sp.Popen(["ffmpeg", "-i","-", "-vcodec", "rawvideo", "-pix_fmt", "yuv420p", "-threads", "0", "-f", "v4l2", "/dev/video0"], stdin=sp.PIPE, stdout=sp.PIPE)


#         # timer for getting frames

#         # while True:
#         #     ret, frame = self.cap.read()
#         #     # print("num")
#         #     if ret:
#         #         print(frame)
#         #         rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         #         h, w, ch = rgbImage.shape
#         #         bytesPerLine = ch * w
#         #         convertToQtFormat = QtGui.QImage(rgbImage.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
#         # #         # p = convertToQtFormat.scaled(1250, 1000, Qt.KeepAspectRatio)
#         # #         self.changePixmap.emit(p)

#         #         convertToQtFormat = QtGui.QPixmap.fromImage(convertToQtFormat)
#         #         pixmap = QtGui.QPixmap(convertToQtFormat)
#         #          = pixmap.scaled(1250, 1000, QtCore.Qt.KeepAspectRatio)
#         # #         # QApplication.processEvents()
#         #         self.label.setPixmap(resizeImage)
#         #         self.show()
        
#         # self.destroy()) # quiter button 
#     # def run(self): 

        

#     def initLayout(self):
        
#         # p = sp.Popen(["gphoto2", "--stdout", "--capture-movie", "|", "ffmpeg", "-i", "-", "-vcodec", "rawvideo", "-pix_fmt", "yuv420p", "-threads", "0", "-f", "v4l2", "/dev/video0"])

#         # sout, _ = p.communicate()
#         # p.wait()
#         #create a label
#         label = QLabel(self)
       
#         # convertToQtFormat = QtGui.QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0],
#                                          # QtGui.QImage.Format_RGB888)
#         cap = cv2.VideoCapture(0)
#         while True:
#             ret, frame = cap.read()
#             # print("num")
#             if ret:
#                 print(frame)
#                 rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#                 h, w, ch = rgbImage.shape
#                 bytesPerLine = ch * w
#                 convertToQtFormat = QtGui.QImage(rgbImage.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
#                 # p = convertToQtFormat.scaled(1250, 1000, Qt.KeepAspectRatio)
#                 self.changePixmap.emit(p)

#                 convertToQtFormat = QtGui.QPixmap.fromImage(convertToQtFormat)
#                 pixmap = QtGui.QPixmap(convertToQtFormat)
#                 resizeImage = pixmap.scaled(1250, 1000, QtCore.Qt.KeepAspectRatio)
#                 # QApplication.processEvents()
#                 label.setPixmap(resizeImage)
#                 self.show()

# class Thread(QtCore.QThread):
#     changePixmap = QtCore.pyqtSignal(QImage)

#     def run(self):
#         cap = cv2.VideoCapture(0)
#         while True:
#             ret, frame = cap.read()
#             if ret:
#                 # https://stackoverflow.com/a/55468544/6622587
#                 rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#                 h, w, ch = rgbImage.shape
#                 bytesPerLine = ch * w
#                 convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
#                 p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
#                 self.changePixmap.emit(p)


class FocusCheckWindow(QWidget):

    def __init__(self, image_dir, main, parent=None):
        super(FocusCheckWindow, self).__init__(parent)

        # Set main window properties
        self.setGeometry(250, 250, 1400, 1400)
        self.setWindowTitle('Focus Check Window')

        self.image_dir = image_dir
        self.main_window = main
     
        self.setLayout(self.initLayout())

    def initLayout(self):
        loader = QtGui.QImage()
        scatter_label = QLabel("Loading...")
        loader.load(os.path.join(self.image_dir, self.main_window.scatter_path + '.jpg'))

        map = QtGui.QPixmap(loader)
        scaled_map = map.scaled(1400, 1400, QtCore.Qt.KeepAspectRatio)
        scatter_label.setPixmap(scaled_map)

        layout = QGridLayout()
        layout.addWidget(scatter_label, 0, 0)
       
        return layout
        
        

class CenterPointWindow(QWidget):

    def __init__(self, image_dir, backup_dir, main, parent=None):
        super(CenterPointWindow, self).__init__(parent)

        # Set main window properties
        self.setGeometry(250, 250, 1600, 700)
        self.setWindowTitle('Center Point Window')

        self.image_dir = image_dir
        self.backup_dir = backup_dir
        self.main_window = main
        self.position = [0,0]

        self.block_size_rescale = 8
        # self.cropped_size = [1600, 2400]

        self.cropped_size = [2496, 3504]

        self.setLayout(self.initLayout())
        
        
    def initLayout(self):
        self.accept_button = QPushButton('Accept Center Point')
        self.position_label = QLabel("Center Point: ")
        
        #################################
        self.scatter_title = QLabel("Scatter Image")
        self.scatter_cropped_title = QLabel("Cropped Scatter Image")
        self.scatter_label = QLabel("Loading...")
        self.scatter_cropped_label = QLabel("Loading...")
        #################################

        # Set the line edits for the block size
        self.block_size_label = QLabel("Block Size")
        self.block_size = ["Large", "Standard"]
        self.block_size_drop = QComboBox()
        self.block_size_drop.addItems(self.block_size)
        
        self.block_size_drop.setCurrentIndex(self.block_size.index('Large'))


        self.loop = QtCore.QEventLoop()
        
        #################################

        # self.retake_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.accept_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.position_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Connect the button
        self.accept_button.clicked.connect(self.acceptClicked)
        # self.retake_button.clicked.connect(self.retakeClicked)
        self.accept_button.clicked.connect(self.loop.quit)

        # Initially disable the accept button until image has been validated
        # self.accept_button.setDisabled(True)

        #################################
        self.scatter_title.setAlignment(QtCore.Qt.AlignCenter)
        self.scatter_cropped_title.setAlignment(QtCore.Qt.AlignCenter)

        self.scatter_label.setAlignment(QtCore.Qt.AlignCenter)
        self.scatter_cropped_label.setAlignment(QtCore.Qt.AlignCenter)
        #################################


        gridLayout = QGridLayout()
        # gridLayout.addWidget(self.retake_button, 0, 0)
        gridLayout.addWidget(self.accept_button, 0, 0, 1,2)
        gridLayout.addWidget(self.position_label, 2, 0, 1, 2)
        gridLayout.addWidget(self.block_size_label, 1, 0, 1, 1)
        gridLayout.addWidget(self.block_size_drop, 1, 1, 1, 1)


        imageLayout = QGridLayout()
        imageLayout.addWidget(self.scatter_title, 0, 0)
        imageLayout.addWidget(self.scatter_label, 1, 0)
        imageLayout.addWidget(self.scatter_cropped_title, 0, 1)
        imageLayout.addWidget(self.scatter_cropped_label, 1, 1)
        

        ###############################

        gridLayout.setRowStretch(1, 0)
        imageLayout.setRowStretch(4, 0)

        # gridLayout.setColumnStretch(1, 5)
        # imageLayout.setColumnStretch(4, 30)

        layout = QGridLayout()
        layout.addLayout(gridLayout, 0, 0)
        layout.addLayout(imageLayout, 0, 1)
        layout.setColumnStretch(1, 6)

        return layout

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.LeftButton:
            event.accept()

            _localPos = event.localPos()
            # print(self.scatter_label.x(), self.scatter_label.y())

            if(self.block_size_drop.currentText()=="Large"):
                self.block_size_rescale = 8
                # self.cropped_size = [1600, 2400]
                self.cropped_size = [2496, 3504]
                pass
            elif(self.block_size_drop.currentText()=="Standard"):
                self.block_size_rescale = 8
                # self.cropped_size = [1500, 1000]
                self.cropped_size = [1800, 1200]
                pass
            else:
                self.scatter_cropped_label.setText("Block Size Error! \n Do not continue before Fixed!")
          
            ####### a several pixels margin in the label is ignored, since the position don't need pixel level acc.
            ####### QPixmap is 8x downsampled. 
            
            self.position = [(_localPos.x()-self.scatter_label.x())*self.block_size_rescale, (_localPos.y()-self.scatter_label.y())*self.block_size_rescale]

            if(int(self.position[1]-self.cropped_size[1]/2)<0 or int(self.position[1]+self.cropped_size[1]/2)>self.loader.height() or int(self.position[0]-self.cropped_size[0]/2)<0 or int(self.position[0]+self.cropped_size[0]/2)>self.loader.width()):
                self.position_label.setText("Center Point too close to bord!")
                return

            self.position_label.setText("Center Point (x, y): " + str([self.position]))
            # print(_localPos.x(),self.scatter_label.x(), self.cropped_size[0]/self.block_size_rescale/2)
            # print(_localPos.y(), self.scatter_label.y(), self.cropped_size[1]/self.block_size_rescale/2, self.cropped_size[0], self.cropped_size[1])

            ####### We take a 2400x1600 rect as input for segmentation, same 8x downsampled for these value.

            rect = QtCore.QRect((_localPos.x()-self.scatter_label.x()-self.cropped_size[0]/self.block_size_rescale/2), (_localPos.y()-self.scatter_label.y()-self.cropped_size[1]/self.block_size_rescale/2), self.cropped_size[0]/self.block_size_rescale, self.cropped_size[1]/self.block_size_rescale)

            cropQPixmap = self.scaled_map.copy(rect)
            self.scatter_cropped_label.setPixmap(cropQPixmap)

        else:
            event.ignore()
            return

    def getCenter(self):
        self.loader = QtGui.QImage()
        print(self.image_dir + '/' + self.main_window.scatter_path + '.jpg')
        self.loader.load(self.image_dir + '/' + self.main_window.scatter_path + '.jpg')  
        # print(self.loader.size().width(), self.loader.size().height())

        map = QtGui.QPixmap(self.loader)
        self.scaled_map = map.scaled(self.loader.size().width()/self.block_size_rescale, self.loader.size().height()/self.block_size_rescale, QtCore.Qt.KeepAspectRatio)            # resize scatter image to 750x500, original size 6000x4000
        self.scatter_label.setPixmap(self.scaled_map)

        # print(self.position)


    def acceptClicked(self):
        # Reject invalid position
        # if(int(self.position[1]-self.cropped_size[1]/2)<0 or int(self.position[1]+self.cropped_size[1]/2)>self.loader.height() or int(self.position[0]-self.cropped_size[0]/2)<0 or int(self.position[0]+self.cropped_size[0]/2)>self.loader.width()):
        #     self.position_label.setText("Center Point too close to bord!")
        #     return

        msg = "Center Point Provided!!!"
        self.main_window.main_label.setText(msg)
        self.main_window.main_label.setStyleSheet("color: white")

        # Need to re-enable the main window
        self.main_window.setDisabled(False)
        # Make sure all the buttons have been restored to enable
        # self.main_window.hit_button.setDisabled(False)
        self.main_window.trim_button.setDisabled(False)
        self.main_window.sect_button.setDisabled(False)
        self.main_window.main_table.setDisabled(False)

        

        self.main_window.center_point_f.write(str(self.position[0]) + ',' + str(self.position[1]) + ',' + str(self.cropped_size[0]) + ',' + str(self.cropped_size[1]) + ',' + str(self.block_size_rescale))
        self.main_window.position = self.position
        self.main_window.cropped_size = self.cropped_size
        self.main_window.block_size_rescale = self.block_size_rescale
        
        self.close()
        self.destroy()


    def closeEvent(self, event):
        # print("position:", self.position == [0,0])
        if (self.position == [0,0]):
            # remove the center_point.txt
            self.main_window.center_point_f.close()
            os.remove(self.main_window.image_dir + '/csv_files/center_point.txt')

        event.accept()


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


class ImageWindow(QWidget):

    def __init__(self, image_dir, backup_dir, main, parent=None):
        super(ImageWindow, self).__init__(parent)

        # Set main window properties
        self.setGeometry(200, 200, 1600, 400)
        self.setWindowTitle('Image Window')

        self.image_dir = image_dir
        self.backup_dir = backup_dir
        self.main_window = main

        self.flag = False
        self.draw_en = False
        self.button_bk_en = False
        self.button_fg_en = False
        self.box_accept_flag = False
        self.press_event = False
        self.move_event = False

        self.bk_list = []
        self.fg_list = []
        self.rescale_size = 4.0

        self.setLayout(self.initLayout())


    def initLayout(self):
        self.retake_button = QPushButton('Retake Image')
        self.accept_button = QPushButton('Accept Image')
        self.section_a = QCheckBox('Section a')
        self.section_b = QCheckBox('Section b')
        self.section_c = QCheckBox('Section c')
        self.iso_label = QLabel("ISO: ")
        self.fstop_label = QLabel("FStop: ")
        self.ss_label = QLabel("SS: ")
        self.surface_label = QLabel("Loading...")
        self.scatter_label = QLabel("Loading...")
        self.surface_title = QLabel("Surface Image")
        self.scatter_title = QLabel("Scatter Image")

        #################################
        self.cropped_scatter_label = QLabel("Loading...")
        self.scatter_mask_label = QLabel("Loading...")
        self.cropped_scatter_title = QLabel("Cropped Scatter Image")
        self.scatter_mask_title = QLabel("LDA Result")

        # self.cnn_mask_label = QLabel("Loading...")
        # self.cnn_mask_title = QLabel("1CN Result")
        #################################

        self.notes_edit = QLineEdit("No notes")
        self.bk = QPushButton("Background")
        # self.bk_2 = QPushButton("BK_2")
        self.fg = QPushButton("Foreground")
        # self.size_lable = QLabel("size:")
        # self.size_val = QLineEdit("100")
        self.box_accept = QPushButton("Accept Boxes")

        self.retake_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.accept_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.section_a.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.section_b.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.section_c.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.iso_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.fstop_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.ss_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.notes_edit.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        # self.load_image_button.clicked.connect(self.selectNewImage)
        self.bk.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        # self.bk_2.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.fg.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        # self.size_lable.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        # self.size_val.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.box_accept.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        # Check to see if the the sections have been taken yet
        if self.main_window.section_a:
            self.section_a.setChecked(True)
            self.section_a.setDisabled(True)

        if self.main_window.section_b:
            self.section_b.setChecked(True)
            self.section_b.setDisabled(True)

        if self.main_window.section_c:
            self.section_c.setChecked(True)
            self.section_c.setDisabled(True)

        # Connect the button
        self.accept_button.clicked.connect(self.acceptClicked)
        self.retake_button.clicked.connect(self.retakeClicked)

        self.bk.clicked.connect(self.getbox_bk)
        self.fg.clicked.connect(self.getbox_fg)
        self.box_accept.clicked.connect(self.boxs_accept)


        # Initially disable the accept button until image has been validated
        # self.accept_button.setDisabled(True)

        self.surface_label.setAlignment(QtCore.Qt.AlignCenter)
        self.scatter_label.setAlignment(QtCore.Qt.AlignCenter)

        #################################
        self.cropped_scatter_label.setAlignment(QtCore.Qt.AlignLeft)
        self.scatter_mask_label.setAlignment(QtCore.Qt.AlignCenter)
        # self.cnn_mask_label.setAlignment(QtCore.Qt.AlignCenter)
        #################################

        gridLayout = QGridLayout()
        gridLayout.addWidget(self.retake_button, 0, 0, 1, 3)
        gridLayout.addWidget(self.iso_label, 1, 0)
        gridLayout.addWidget(self.fstop_label, 1, 1)
        gridLayout.addWidget(self.ss_label, 1, 2)
        gridLayout.addWidget(self.accept_button, 2, 0, 1, 3)
        gridLayout.addWidget(self.section_a, 3, 0)
        gridLayout.addWidget(self.section_b, 3, 1)
        gridLayout.addWidget(self.section_c, 3, 2)
        gridLayout.addWidget(self.notes_edit, 4, 0, 1, 3)

        gridLayout.addWidget(self.bk, 5, 0)
        # gridLayout.addWidget(self.bk_2, 5, 1)
        gridLayout.addWidget(self.fg, 5, 1)
        # gridLayout.addWidget(self.size_lable, 6, 0)
        # gridLayout.addWidget(self.size_val, 6, 1)
        gridLayout.addWidget(self.box_accept, 5, 2)

        imageLayout = QGridLayout()
        imageLayout.addWidget(self.surface_title, 0, 0)
        imageLayout.addWidget(self.surface_label, 1, 0)
        imageLayout.addWidget(self.scatter_title, 0, 1)
        imageLayout.addWidget(self.scatter_label, 1, 1)

        ###############################
        maskLayout = QGridLayout()
        maskLayout.addWidget(self.cropped_scatter_title, 0, 0)
        maskLayout.addWidget(self.cropped_scatter_label, 1, 0)
        maskLayout.addWidget(self.scatter_mask_title, 0, 1)
        maskLayout.addWidget(self.scatter_mask_label, 1, 1)

        # maskLayout.addWidget(self.cnn_mask_title, 0, 2)
        # maskLayout.addWidget(self.cnn_mask_label, 1, 2)
        ###############################

        maskLayout.setRowStretch(0, 5)
        maskLayout.setRowStretch(0, 30)

        layout = QGridLayout()
        layout.addLayout(gridLayout, 0, 0, 2, 1)
        layout.addLayout(imageLayout, 0, 1)
        layout.addLayout(maskLayout, 1, 1)
        
        # layout.setColumStretch(0, 10)
        # layout.setRowStretch(1, 15)
        # self.surface_label.setText(self.image_path)

        return layout


     ####### We take a 2400x1600 rect as input for segmentation, same 6x downsampled for these value (map.scaled(400, 400, QtCore.Qt.KeepAspectRatio)).

    def mouseReleaseEvent(self,event):
        
        if self.flag:
            event.accept()
            self.flag = False
            self.draw_en = True

            if(self.button_bk_en):
                self.bk_list.append([(np.array(self.roi_position_tl)*(np.max(self.main_window.cropped_size)/400)).astype(int).tolist(), (np.array(self.roi_position_br)*(np.max(self.main_window.cropped_size)/400)).astype(int).tolist()])      #*6,
                self.button_bk_en = False
                self.move_event = False

            if(self.button_fg_en):
                self.fg_list.append([(np.array(self.roi_position_tl)*(np.max(self.main_window.cropped_size)/400)).astype(int).tolist(), (np.array(self.roi_position_br)*(np.max(self.main_window.cropped_size)/400)).astype(int).tolist()])
                self.button_fg_en = False
                self.move_event = False

            print(self.bk_list)
            try:
                print(self.fg_list[-1])
            except Exception as e:
                print(e)
                print('Empty fg_list!')
            self.update()

    def mouseDoubleClickEvent(self, event):
        event.ignore()
        return

    def mouseMoveEvent(self,event):
        if (self.flag):
            event.accept()
            _localPos = event.localPos()
            # print(self.scatter_label.x(), self.scatter_label.y())
      
            ####### a several pixels margin in the label is ignored, since the position don't need pixel level acc.
            ####### QPixmap is 8x downsampled. 

            # print(_localPos.x(), self.cropped_scatter_label.x(), _localPos.y(), self.cropped_scatter_label.y())
            self.roi_position_br = np.array((_localPos.x()-self.cropped_scatter_label.x(), _localPos.y()-self.cropped_scatter_label.y()), dtype=int).squeeze()

       # self.x1 = event.x()
       # self.y1 = event.y()
            self.update()

    def mousePressEvent(self, event):
        if self.flag and event.button() == QtCore.Qt.LeftButton:
            # self.size = int(self.size_val.text()) / 6.0
            # print(self.size, self.bk1_tl)
            event.accept()
            _localPos = event.localPos()
            # print(self.scatter_label.x(), self.scatter_label.y())
          
            ####### a several pixels margin in the label is ignored, since the position don't need pixel level acc.
            ####### QPixmap is 8x downsampled. 

            print(_localPos.x(), self.cropped_scatter_label.x(), _localPos.y(), self.cropped_scatter_label.y())
            self.roi_position_tl = np.array((_localPos.x()-self.cropped_scatter_label.x(), _localPos.y()-self.cropped_scatter_label.y()), dtype=int).squeeze()
            print("Box Point (x, y): " + str([self.roi_position_tl]))

            # if(self.button_bk1_en == 1):
            #     self.bk1_tl = (np.array(self.roi_position) - int(self.size / 2)).astype(np.int) * 6
            #     self.button_bk1_en = 0
            # elif(self.button_bk2_en == 1):
            #     self.bk2_tl = (np.array(self.roi_position) - int(self.size / 2)).astype(np.int) * 6
            #     self.button_bk2_en = 0
            # elif(self.button_fg1_en == 1):
            #     self.fg1_tl = (np.array(self.roi_position) - int(self.size / 2)).astype(np.int) * 6
            #     self.button_fg1_en = 0
         
            # self.cropped_scatter_label.setCursor(QtCore.Qt.CrossCursor)

            # rect = QtCore.QRect((_localPos.x()-self.scatter_label.x()-150), (_localPos.y()-self.scatter_label.y()-125), 300, 200)

            # cropQPixmap = self.scaled_map.copy(rect)
            # self.scatter_mask_label.setPixmap(cropQPixmap)
        else:
            event.ignore()
            return

    def paintEvent(self, event):
        if(self.draw_en):
            # print("Start!")
           
            pixmap = QtGui.QPixmap(self.scaled_roi_painted.size())
            pixmap.fill(QtCore.Qt.transparent)

            painter = QtGui.QPainter(self.scaled_roi_painted)

            painter.setPen(QtGui.QPen(QtCore.Qt.green, 3, QtCore.Qt.SolidLine))
            # print("paint start point:", self.cropped_scatter_label.x(), self.cropped_scatter_label.y())
            # print(self.roi_position_tl[0], self.roi_position_tl[1], self.roi_position_br[0]-self.roi_position_tl[0], self.roi_position_br[1]-self.roi_position_tl[1])
            painter.drawRect(self.roi_position_tl[0], self.roi_position_tl[1], self.roi_position_br[0]-self.roi_position_tl[0], self.roi_position_br[1]-self.roi_position_tl[1])
            # painter.drawRect(self.cropped_scatter_label.x(), self.cropped_scatter_label.y(),20,20)

            painter.end()
            self.cropped_scatter_label.setPixmap(self.scaled_roi_painted)

            self.draw_en = False  

    def getbox_bk(self):
        if (self.box_accept_flag):
            # reload the img
            # print("reloading!")
            self.cropped_scatter_label.setPixmap(self.scaled_roi_tmp)
            self.box_accept_flag = False
            # self.update()

        self.flag = True
        self.button_bk_en = True
        # self.bk1_tl = (self.roi_position - (self.size / 2)) * 6

    def getbox_fg(self):
        if (self.box_accept_flag):
            # reload the img
            self.cropped_scatter_label.setPixmap(self.scaled_roi_tmp)
            self.box_accept_flag = False
            # self.update()

        self.flag = True
        self.button_fg_en = True
        # self.fg1_tl = (self.roi_position - (self.size / 2)) * 6
        
    def boxs_accept(self):
        # if(self.bk1_tl!=[0,0] and self.bk2_tl!=[0,0] and self.fg1_tl!=[0,0]):
        self.box_accept_flag = True 
        self.scaled_roi_painted = self.scaled_roi_tmp.copy()

        if(len(self.fg_list) >1):
            self.bk_list.append(self.fg_list[-1])
        elif(len(self.fg_list) >0):
            self.bk_list.append(self.fg_list[0])
        else:
            pass
        # print(self.bk_list, self.image_dir, self.main_window.scatter_path.split("_")[1])
        # tmp_scatter_roi = rescale(self.scatter_roi, 1/6.0, multichannel=True, anti_aliasing=True)

        # self.bk_list = [(val * (np.max(self.main_window.cropped_size) / 400)).astype(int) for val in self.bk_list]
        # list((np.array(self.bk_list) * (np.max(self.main_window.cropped_size) / 400)).astype(int))
        print(self.bk_list)

        
        lda_input = skimage.transform.rescale(self.scatter_roi, 1/self.rescale_size, multichannel=True, anti_aliasing=True)
        for x in range(len(self.bk_list)):
            for i in range(len(self.bk_list[x])):
                for y in range(len(self.bk_list[x][i])):
                    self.bk_list[x][i][y] = int(self.bk_list[x][i][y]/self.rescale_size)
        print("After",self.bk_list)
        try:
            mask = segmenation_LDA(lda_input, self.bk_list, self.image_dir, self.main_window.scatter_path.split("_")[1])
            if(np.max(mask)==0):
                self.scatter_mask_label.setText("Reselect the BK & FG!")
                print("Reselect the BK & FG!")

            else:
                _mask = qimage2ndarray.array2qimage((255*(mask/np.max(mask))).astype(np.uint8))
                map = QtGui.QPixmap.fromImage(_mask)
                scaled_map = map.scaled(400, 400, QtCore.Qt.KeepAspectRatio)
                self.scatter_mask_label.setPixmap(scaled_map)
        except Exception as e:
            print(e)
            print("#######    ERROR! PLEASE RESELECT REGIONS    #######")
            self.scatter_mask_label.setText("Reselect the BK & FG!")

       
        # print("class:{}".format(set(mask.flatten())))

        # Remove the patch info (in case users not satisfied with the prediction & wish to redo the patch select)
        self.bk_list.clear()
        self.fg_list.clear()
        # mask = segmenation_LDA(self.scatter_roi, self.bk1_tl, self.bk1_tl, self.bk1_tl, int(self.size_val.text()))

        # imageio.imwrite(os.path.join(self.image_dir, "scatter_mask_tmp.jpg"), Image.fromarray((np.argmax(mask, axis=0) * 255 / mask.shape[0]).astype(np.uint8)))
       

   
    def loadImage(self):

        loader = QtGui.QImage()
        # print(self.image_dir + '/' + self.main_window.scatter_path + '.jpg')
        loader.load(os.path.join(self.image_dir, self.main_window.surface_path + '.jpg'))

        map = QtGui.QPixmap(loader)
        scaled_map = map.scaled(400, 400, QtCore.Qt.KeepAspectRatio)
        self.surface_label.setPixmap(scaled_map)

        loader.load(os.path.join(self.image_dir, self.main_window.scatter_path + '.jpg'))

        map = QtGui.QPixmap(loader)
        scaled_map = map.scaled(400, 400, QtCore.Qt.KeepAspectRatio)
        self.scatter_label.setPixmap(scaled_map)

      
        ############ Calculate Mask Here ##################
        # print(os.path.join(self.image_dir, self.main_window.scatter_path + '.jpg'))
        # print(self.main_window.scatter_path)
        
        # if(int(self.main_window.scatter_path.split("_")[1]) > 1):
        ####### Change different seg methods and dependence here
        # scatter_name = self.image_dir + "/" + self.main_window.scatter_path + ".jpg"
        scatter_name_nef = self.image_dir + "/" + self.main_window.scatter_path + '.nef'

        # scatter_name_nef = self.image_dir + "/" + "IMG_0004_scatter.nef"
        # scatter_name_nef = "/home2/tester/Desktop/Storage_1/IACUC2049/C11-R03/01/" + "IMG_0053_scatter.nef"
        # print(scatter_name_nef)
        
        # scatter_name = self.image_dir + "/test_input.jpg"
        # scatter_img = imageio.imread(scatter_name)

        # scatter_name_nef = self.image_dir + "/IMG_0021_scatter.nef"
        scatter_img = rawpy.imread(scatter_name_nef).postprocess()
        
        # print(int(self.main_window.position[1]), self.main_window.cropped_size[1]/2, int(self.main_window.position[1]), self.main_window.cropped_size[1]/2, int(self.main_window.position[0]), self.main_window.cropped_size[0]/2, int(self.main_window.position[0]), self.main_window.cropped_size[0]/2)
        # print(int(self.main_window.position[1]-self.main_window.cropped_size[1]/2), int(self.main_window.position[1]+self.main_window.cropped_size[1]/2), int(self.main_window.position[0]-self.main_window.cropped_size[0]/2), int(self.main_window.position[0]+self.main_window.cropped_size[0]/2))

        self.scatter_roi = scatter_img[int(self.main_window.position[1]-self.main_window.cropped_size[1]/2):int(self.main_window.position[1]+self.main_window.cropped_size[1]/2), int(self.main_window.position[0]-self.main_window.cropped_size[0]/2):int(self.main_window.position[0]+self.main_window.cropped_size[0]/2), :]

        roi_image = qimage2ndarray.array2qimage(self.scatter_roi)
        self.roi_map = QtGui.QPixmap.fromImage(roi_image)


        # imageio.imwrite(os.path.join(self.image_dir, "scatter_roi_tmp.jpg"), self.scatter_roi)
        # print(os.path.join(self.image_dir, "scatter_roi_tmp.jpg"))

        # ####### Load the mask image to GUI
        # loader = QtGui.QImage()
        # loader.load(self.image_dir + '/scatter_roi_tmp.jpg')

        # map = QtGui.QPixmap(loader)
        self.scaled_roi_tmp = self.roi_map.scaled(400, 400, QtCore.Qt.KeepAspectRatio)
        self.cropped_scatter_label.setPixmap(self.scaled_roi_tmp)
        self.scaled_roi_painted = self.scaled_roi_tmp.copy()

        # Select ROI 
        ####### We take a 2400x1600 rect as input for segmentation, same 6x downsampled for these value (map.scaled(400, 400, QtCore.Qt.KeepAspectRatio)).
        
        # loader.load(self.image_dir + '/scatter_mask_tmp.jpg')
        # map = QtGui.QPixmap(loader)
        # scaled_map = map.scaled(400, 400, QtCore.Qt.KeepAspectRatio)
        # self.scatter_mask_label.setPixmap(scaled_map)


        # ### Get the pre_scatter ###
        # pre_scatter_num = int(self.main_window.scatter_path.split("_")[1]) - 1
        # pre_scatter_name = self.main_window.scatter_path.split("_")[0] + "_" + str(pre_scatter_num).zfill(4) + "_" + self.main_window.scatter_path.split("_")[2]
        # print(pre_scatter_name)

        # scatter_name_1 = self.image_dir + '/' + pre_scatter_name + ".png"
        # scatter_name_2 = self.image_dir + "/" + self.main_window.scatter_path + ".png"

        # scatter_1 = imageio.imread(scatter_name_1)
        # scatter_2 = imageio.imread(scatter_name_2)

        # scatter_diff = scatter_2 - scatter_1
        # self.scatter_diff_roi = scatter_diff[int(self.main_window.position[1])-800:int(self.main_window.position[1])+800, int(self.main_window.position[0])-1200:int(self.main_window.position[0])+1200, :]

        # print("Segmentation!    Calling Unet!")
        # self.segmentation()

        # ####### Load the mask image to GUI
        # loader = QtGui.QImage()
        # loader.load(self.image_dir + '/scatter_diff_roi_tmp.png')

        # map = QtGui.QPixmap(loader)
        # scaled_map = map.scaled(400, 400, QtCore.Qt.KeepAspectRatio)
        # self.cropped_scatter_label.setPixmap(scaled_map)

        # loader.load(self.image_dir + '/scatter_mask_tmp.png')

        # map = QtGui.QPixmap(loader)
        # scaled_map = map.scaled(400, 400, QtCore.Qt.KeepAspectRatio)
        # self.scatter_mask_label.setPixmap(scaled_map)
        # print("index", self.main_window.scatter_path.split("_")[1], int(self.main_window.scatter_path.split("_")[1]))

        # if(int(self.main_window.scatter_path.split("_")[1]) > 1):
            # try:
        lda_input = skimage.transform.rescale(self.scatter_roi, 1/self.rescale_size, multichannel=True, anti_aliasing=True)
       
        try:
            mask = segmenation_LDA(lda_input, [], self.image_dir, self.main_window.scatter_path.split("_")[1])
            if(np.max(mask)==0):
                self.scatter_mask_label.setText("Reselect the BK & FG!")
                print("Reselect the BK & FG!")

            else:
                _mask = qimage2ndarray.array2qimage((255*(mask/np.max(mask))).astype(np.uint8))
                map = QtGui.QPixmap.fromImage(_mask)
                scaled_map = map.scaled(400, 400, QtCore.Qt.KeepAspectRatio)
                self.scatter_mask_label.setPixmap(scaled_map)
        except Exception as e:
            print(e)
            print("#######    ERROR! PLEASE RESELECT REGIONS    #######")
            self.scatter_mask_label.setText("Reselect the BK & FG!")


        ##############################

      
        # How long does metadata take
        # Metat data is a namedtuple container
        # with pyexiv2.ImageMetadata(self.image_dir + '/' + self.main_window.surface_path + '.nef') as raw:
        raw_surface = pyexiv2.ImageMetadata(self.image_dir + '/' + self.main_window.surface_path + '.nef')
            # raw_img = exif.Image(raw)
        raw_surface.read()
        
        self.iso_loaded_surface = raw_surface["Exif.Photo.ISOSpeedRatings"].value
        self.ss_loaded_surface = raw_surface["Exif.Photo.ExposureTime"].value
        self.fstop_loaded_surface = raw_surface["Exif.Photo.FNumber"].value
        # Convert the shutter speed to a number
        # self.ss_loaded_surface = int(np.ceil(1 / self.ss_loaded_surface))
        # self.validateSurfaceImage()


        raw_scatter = pyexiv2.ImageMetadata(self.image_dir + '/' + self.main_window.scatter_path + '.nef')
           
        raw_scatter.read()
     
        self.iso_loaded_scatter = raw_scatter["Exif.Photo.ISOSpeedRatings"].value
        self.ss_loaded_scatter = raw_scatter["Exif.Photo.ExposureTime"].value
        self.fstop_loaded_scatter = raw_scatter["Exif.Photo.FNumber"].value
        # Convert the shutter speed to a number
        # self.ss_loaded_scatter = int(np.ceil(1 / self.ss_loaded_scatter))
        # self.validateScatterImage()

        ###### rawkit is deprecated ######
        
        # with Raw(filename=self.image_dir + '/' + self.main_window.surface_path + '.nef') as raw:
        #     self.iso_loaded_surface = raw.metadata.iso
        #     self.ss_loaded_surface = raw.metadata.shutter
        #     self.fstop_loaded_surface = np.around(raw.metadata.aperture, 1)
        # # Convert the shutter speed to a number
        # # self.ss_loaded_surface = int(np.ceil(1 / self.ss_loaded_surface))
        # # self.validateSurfaceImage()

        # with Raw(filename=self.image_dir + '/' + self.main_window.scatter_path + '.nef') as raw:
        #     self.iso_loaded_scatter = raw.metadata.iso
        #     self.ss_loaded_scatter = raw.metadata.shutter
        #     self.fstop_loaded_scatter = np.around(raw.metadata.aperture, 1)
        # # Convert the shutter speed to a number
        # # self.ss_loaded_scatter = int(np.ceil(1 / self.ss_loaded_scatter))
        # # self.validateScatterImage()

        self.iso_label.setText("ISO: " + str([self.iso_loaded_surface, self.iso_loaded_scatter]))
        self.fstop_label.setText("FStop: " + str([self.fstop_loaded_surface, self.fstop_loaded_scatter]))
        self.ss_label.setText("SS: " + str([self.ss_loaded_surface, self.ss_loaded_scatter]))

    def validateSurfaceImage(self):

        # Check the iso values
        iso = self.main_window.iso_drop_surface.currentText() == str(int(self.iso_loaded_surface))
        # Check the shutter speed
        ss = self.main_window.ss_drop_surface.currentText() == str(self.ss_loaded_surface)
        # Check the fstop
        fstop = self.main_window.fstop_drop_surface.currentText() == str(self.fstop_loaded_surface)

        # If the image is valid, let them accept
        if fstop and ss and iso:
            self.accept_button.setDisabled(False)

        else:
            msg = 'Image parameters for the surface image are not correct!\n'
            msg += 'ISO:  ' + str(int(self.iso_loaded_surface))
            msg += '  should be  ' + self.main_window.iso_drop_surface.currentText() + '\n'
            msg += 'FStop:  ' + str(self.fstop_loaded_surface)
            msg += '  should be  ' + self.main_window.fstop_drop_surface.currentText() + '\n'
            msg += 'SS:  ' + str(self.ss_loaded_surface)
            msg += '  should be  ' + self.main_window.ss_drop_surface.currentText() + '\n'
            msg += 'Please retake the image!'
            self.errorMessage(msg)

    def validateScatterImage(self):

        # Check the iso values
        iso = self.main_window.iso_drop_scatter.currentText() == str(int(self.iso_loaded_scatter))
        # Check the shutter speed
        ss = self.main_window.ss_drop_scatter.currentText() == str(self.ss_loaded_scatter)
        # Check the fstop
        fstop = self.main_window.fstop_drop_scatter.currentText() == str(self.fstop_loaded_scatter)

        # If the image is valid, let them accept
        if fstop and ss and iso:
            self.accept_button.setDisabled(False)

        else:
            msg = 'Image parameters for the scatter image are not correct!\n'
            msg += 'ISO:  ' + str(int(self.iso_loaded_scatter))
            msg += '  should be  ' + self.main_window.iso_drop_scatter.currentText() + '\n'
            msg += 'FStop:  ' + str(self.fstop_loaded_scatter)
            msg += '  should be  ' + self.main_window.fstop_drop_scatter.currentText() + '\n'
            msg += 'SS:  ' + str(self.ss_loaded_scatter)
            msg += '  should be  ' + self.main_window.ss_drop_scatter.currentText() + '\n'
            msg += 'Please retake the image!'
            self.errorMessage(msg)

    def _rowConstructor(self, note=None):

        self.section_list = ''
        if self.section_a.isChecked() and self.section_a.isEnabled():
            if self.main_window.section_count == 0:
                self.main_window.section_count = 1
                self.main_window.section_start = self.main_window.total_distance - 50
            self.section_list += str(self.main_window.section_count) + 'a;'
            self.main_window.section_a = True
            self.main_window.started_sects = True
        if self.section_b.isChecked() and self.section_b.isEnabled():
            if self.main_window.section_count == 0:
                self.main_window.section_count = 1
                self.main_window.section_start = self.main_window.total_distance - 50
            self.section_list += str(self.main_window.section_count) + 'b;'
            self.main_window.started_sects = True
            self.main_window.section_b = True
        if self.section_c.isChecked() and self.section_c.isEnabled():
            if self.main_window.section_count == 0:
                self.main_window.section_count = 1
                self.main_window.section_start = self.main_window.total_distance - 50
            self.section_list += str(self.main_window.section_count) + 'c;'
            self.main_window.started_sects = True
            self.main_window.section_c = True

        if self.main_window.section_a and self.main_window.section_b and self.main_window.section_c:
            self.main_window.section_a = False
            self.main_window.section_b = False
            self.main_window.section_c = False
            msg = "<font color=green>Everything Nominal</font>"
            self.main_window.main_label.setText(msg)
            self.main_window.section_count += 1

        if self.section_list == '':
            self.section_list = 'None'

        # Construct the new row to the table as a list of strings
        # get rid of the .CR2
        if note is not None:
            notes = self.notes_edit.text() + ' - ' + note
        else:
            notes = self.notes_edit.text()

        self.main_window.table_list.append([
            [self.main_window.surface_path.split('/')[-1].split('.')[0],
             self.main_window.scatter_path.split('/')[-1].split('.')[0]],
            str(self.main_window.total_distance),
            self.section_list,
            [str(self.ss_loaded_surface)[0:7], str(self.ss_loaded_scatter)[0:7]],
            [str(self.iso_loaded_surface), str(self.iso_loaded_scatter)],
            [str(self.fstop_loaded_surface), str(self.fstop_loaded_scatter)],
            notes
        ])

        # Add a new row to the table
        rowPosition = self.main_window.main_table.rowCount()
        self.main_window.main_table.insertRow(rowPosition)

        # Populate the new row
        for i, col in enumerate(self.main_window.table_list[-1]):
            item = QTableWidgetItem(str(col))
            self.main_window.main_table.setItem(rowPosition, i, item)

    def acceptClicked(self):
        # Need to reset the image_distance
        self.main_window.image_distance = 0
        self.main_window.image_dist_label.setText('Image Distance: ' + str(0) + ' μm')
        # Reset the hit button text to what it was before
        self.main_window.trim_button.setText("TRIM (50 μm)")
        self.main_window.trim_button.setStyleSheet("color: white")
        self.main_window.sect_button.setText("SECTION (5 μm)")
        self.main_window.sect_button.setStyleSheet("color: white")

        # msg = self.main_window.main_label.text()
        # self.main_window.main_label.setText(msg)

        # Update the main window list with the new row
        self._rowConstructor()

        # Need to re-enable the main window
        self.main_window.setDisabled(False)
        # Make sure all the buttons have been restored to enable
        self.main_window.trim_button.setDisabled(False)
        self.main_window.sect_button.setDisabled(False)
        self.main_window.main_table.setDisabled(False)

        # Need to check if all sections have been taken
        # if self.main_window.section_a and self.main_window.section_b and self.main_window.section_c:
        #     # Update the group section counter
        #     # This is going to incrament every time
        #     # Only update if 'should be taking sections'
        #     # temp = "<font color=red size=40>You should be taking sections</font>"
        #     # if self.main_window.main_label.text() == temp:
        #     #     self.main_window.section_count += 1
        #     if self.main_window.taking_sections:
        #         self.main_window.section_count += 1
        #         self.main_window.taking_sections = False
        #     # Update the main message
        #     msg = "<font color=green>Everything Nominal</font>"
        #     self.main_window.main_label.setText(msg)
        #     # Set the section trackers back to False
        #     self.section_a = False
        #     self.section_b = False
        #     self.section_c = False
        # else:
        #     msg = "<font color=red size=20>You should be taking sections</font>"
        #     self.main_window.main_label.setText(msg)
        # if self.main_window.total_distance == 0:
        #     msg = "<font color=green>Everything Nominal</font>"
        #     self.main_window.main_label.setText(msg)

        if self.main_window.retake:
            msg = "<font color=green>Everything Nominal</font>"
            self.main_window.main_label.setText(msg)
            self.main_window.retake = False
        
        # if (self.main_window.total_distance - self.main_window.section_start) % 250 == 0:
        #     if (self.main_window.total_distance - self.main_window.section_start) == 0:
        #         pass
        #     else:
        #         msg = "<font color=red size=40>You should be taking sections</font>"
        #         self.main_window.main_label.setText(msg)

        if self.main_window.started_sects:
            if (self.main_window.total_distance - self.main_window.section_start) % 250 == 0:
                msg = "<font color=red size=40>You should be taking sections</font>"
                self.main_window.main_label.setText(msg)

        self.main_window.retake = False
        
        self.close()
        self.destroy()

    def retakeClicked(self):
        msg = "<font color=red size=40>RE-TAKE THE IMAGE</font>"
        self.main_window.main_label.setText(msg)

        print(self.main_window.main_label.text())

        # Do I need to allow the user to change the image parameteres here?
        self.main_window.setDisabled(False)
        self.main_window.trim_button.setDisabled(True)
        self.main_window.sect_button.setDisabled(True)
        self.main_window.main_table.setDisabled(True)
        self.main_window.capture_button.setEnabled(True)

        self._rowConstructor(note='Images Retaken')

        # Save the row
        self.main_window.retake = True
        # self.main_window.save()
        self.close()
        self.destroy()

    def closeEvent(self, event):
        self.main_window.save()
        self.main_window.backup()

        event.accept()
        
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
