from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QDialog, QFileDialog

import Settings


class SettingsController(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.settings_dialog = QDialog()
        self.settings_dialog.setModal(True)
        self.file_video = None
        self.file_report = None

        self.settings_dialog.ui = Settings.Ui_Dialog()
        self.settings_dialog.ui.setupUi(self.settings_dialog)

        self.settings = QSettings('MyVideoApp', 'App1')

        self.settings_dialog.ui.save_video_path_textField.setText(self.settings.value('save_video_path'))
        self.settings_dialog.ui.save_report_path_textField.setText(self.settings.value('save_report_path'))

        self.settings_dialog.ui.video_path_button.clicked.connect(self.setVideoPath)
        self.settings_dialog.ui.report_path_button.clicked.connect(self.setReportPath)

        self.settings_dialog.ui.dialogButtonBox.accepted.connect(self.save)

        self.settings_dialog.exec_()

    def setVideoPath(self):
        self.file_video = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.file_video = self.file_video + "/"
        self.settings_dialog.ui.save_video_path_textField.setText(self.file_video)

    def setReportPath(self):
        self.file_report = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.file_report = self.file_report + "/"
        self.settings_dialog.ui.save_report_path_textField.setText(self.file_report)

    def save(self):
        if self.file_video is not None:
            self.settings.setValue('save_video_path', self.file_video)
        if self.file_report is not None:
            self.settings.setValue('save_report_path', self.file_report)
