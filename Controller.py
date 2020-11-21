import csv
import os
from random import randint
from subprocess import Popen

from PyQt5 import QtWidgets
from PyQt5.QtChart import QChart, QChartView, QPieSeries
from PyQt5.QtCore import QDir, QUrl, QSettings
from PyQt5.QtGui import QPainter
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QMainWindow, QStyle, QFileDialog

import Gui
import VideoAnalysis
from SettingsController import SettingsController


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Gui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("vehicle recognition")

        # PRINT ==> SYSTEM
        print('System: ' + platform.system())
        print('Version: ' + platform.release())

        self.ui.detail_report_button.setEnabled(False)

        # CHECK USER SETTINGS
        self.settings = QSettings('MyVideoApp', 'App1')

        if self.settings.value('save_video_path') == None:
            self.settings.setValue('save_video_path', 'reports\\video\\')

        if self.settings.value('save_report_path') == None:
            self.settings.setValue('save_report_path', 'reports\\csv\\')

        # DELETE STANDAR TITLE BAR
        # self.setWindowFlags(Qt.CustomizeWindowHint)
        self.setFixedSize(self.size())

        # BUTTONS HANDLERS
        self.ui.btn_upload_video.clicked.connect(self.uploadVideo)
        self.ui.btn_settings.clicked.connect(self.openSettings)
        self.ui.btn_start.clicked.connect(self.startAnalyzing)

        # VIDEO PLAYER
        self.mediaPlayer = QMediaPlayer()
        self.mediaPlayer.setVideoOutput(self.ui.video_player)
        self.ui.playButton.setEnabled(False)
        self.ui.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.ui.playButton.clicked.connect(self.play)
        self.mediaPlayer.durationChanged.connect(self.getDuration)
        self.mediaPlayer.positionChanged.connect(self.getPosition)
        self.ui.positionSlider.sliderMoved.connect(self.updatePosition)

        self.ui.openButton.clicked.connect(self.openFile)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.error.connect(self.handleError)

        self.ui.detail_report_button.clicked.connect(self.openDetailReport)

        self.show()

    def openFile(self):
        self.mediaPlayer.setMedia(QMediaContent(QFileDialog.getOpenFileUrl()[0]))
        self.ui.playButton.setEnabled(True)

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.ui.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.ui.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))

    def handleError(self):
        self.ui.playButton.setEnabled(False)
        self.ui.status_info.setText("Error: " + self.mediaPlayer.errorString())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    # Total video time acquisition
    def getDuration(self, d):
        '''d Is the total length of video captured( ms)'''
        self.ui.positionSlider.setRange(0, d)
        self.ui.positionSlider.setEnabled(True)
        self.displayTime(d)

    # Video real-time location acquisition
    def getPosition(self, p):
        self.ui.positionSlider.setValue(p)
        self.displayTime(self.ui.positionSlider.maximum() - p)

    # Show time remaining
    def displayTime(self, ms):
        minutes = int(ms / 60000)
        seconds = int((ms - minutes * 60000) / 1000)
        self.ui.lab_duration.setText('{}:{}'.format(minutes, seconds))

    def createPieChart(self):
        amount_of_vehicles = self.loadReport()

        series = QPieSeries()
        series.append("Lorries", float(amount_of_vehicles[0]))
        series.append("Cars", float(amount_of_vehicles[1]))
        series.append("Single-track vehicle", float(amount_of_vehicles[2]))
        series.append("Unknown", float(amount_of_vehicles[3]))

        series.setLabelsVisible()

        chart = QChart()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("Ilość pojazdów")

        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)

        lay = QtWidgets.QHBoxLayout(self.ui.chart_widget)
        lay.addWidget(chartView)

    def loadReport(self):
        with open(self.settings.value('save_report_path') + self.report_csv) as f:
            data = [row for row in csv.reader(f)]
            data = [row for row in data]

        lorries = data[1][0].split(';')[0]
        cars = data[1][0].split(';')[1]
        single_tracks = data[1][0].split(';')[2]
        unknowns = data[1][0].split(';')[3]
        return [lorries, cars, single_tracks, unknowns]

    # Update video location with progress bar
    def updatePosition(self, v):
        self.mediaPlayer.setPosition(v)
        self.displayTime(self.ui.positionSlider.maximum() - v)

    def uploadVideo(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie", QDir.homePath())
        self.ui.status_info.setText("Video uploaded, click start")

    def startAnalyzing(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie", QDir.homePath())
        self.ui.status_info.setText("Analyzing in progress, please wait ...")
        print("dodać tutaj algorytm do analizy wideo i wygenerowania pliku wideo i raportu")
        videoAnalysis = VideoAnalysis.Analyser
        self.report_video = fileName.split('/')[-1].replace('.', str(randint(10000, 99999)) + '.')
        videoAnalysis.copyFile(fileName, self.settings.value('save_video_path'), self.report_video)



        self.report_csv = self.report_video.replace('.', '_report.')
        self.report_csv = self.report_csv.split('.')[0]
        self.report_csv = self.report_csv + '.csv'

        videoAnalysis.copyFile('C:\\Users\\kulig\\Desktop\\STUDIA\\SEMESTR 5\\IO\\report.csv', self.settings.value('save_report_path'), self.report_csv)
        self.createPieChart()
        self.mediaPlayer.setMedia(
            QMediaContent(QUrl.fromLocalFile(self.settings.value('save_video_path') + self.report_video)))
        self.ui.playButton.setEnabled(True)
        self.ui.status_info.setText("Raport ready. Please click play to watch")

        self.ui.detail_report_button.setEnabled(True)

    def openSettings(self):
        SettingsController()

    def openDetailReport(self):
        Popen(self.settings.value('save_report_path') + self.report_csv, shell=True)


if __name__ == "__main__":
    import sys
    import platform

    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    sys.exit(app.exec_())


# TODO w settings jak zaczniesz wyszukiwac i wyłączysz to pokazuje się / i to jest zapisywane
# TODO dodać algorytm karola do wyliczania obiektów
# TODO poskładać ładnie klasy
