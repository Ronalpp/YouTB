import sys
import os
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QRadioButton,
    QFileDialog,
    QMessageBox,
    QHBoxLayout,
    QButtonGroup
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from pytube import YouTube

class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('YouTB - YouTube Downloader')
        self.setWindowIcon(QIcon('Logo.png'))
        self.setGeometry(100, 100, 700, 400)
        self.setStyleSheet("background-color: #fff;")

        layout = QVBoxLayout()
        
        title = QLabel('YouTB - YouTube Downloader')
        title.setFont(QFont('Arial', 24))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #000;")
        layout.addWidget(title)
        
        link_label = QLabel('Paste the link here:')
        link_label.setFont(QFont('Arial', 14))
        link_label.setStyleSheet("color: #000; margin-top: 20px;")
        layout.addWidget(link_label)
        
        self.link_input = QLineEdit(self)
        self.link_input.setFont(QFont('Arial', 12))
        self.link_input.setStyleSheet("border: 2px solid #000; border-radius: 15px; padding: 5px;")
        layout.addWidget(self.link_input)
        
        format_label = QLabel('Select format:')
        format_label.setFont(QFont('Arial', 14))
        format_label.setStyleSheet("color: #000; margin-top: 20px;")
        layout.addWidget(format_label)
        
        format_layout = QHBoxLayout()
        self.format_group = QButtonGroup(self)
        
        self.mp4_radio = QRadioButton('MP4')
        self.mp4_radio.setFont(QFont('Arial', 12))
        self.mp4_radio.setStyleSheet("color: #000; margin-right: 50px;")
        self.mp4_radio.setChecked(True)
        format_layout.addWidget(self.mp4_radio)
        self.format_group.addButton(self.mp4_radio)
        
        self.mp3_radio = QRadioButton('MP3')
        self.mp3_radio.setFont(QFont('Arial', 12))
        self.mp3_radio.setStyleSheet("color: #000;")
        format_layout.addWidget(self.mp3_radio)
        self.format_group.addButton(self.mp3_radio)
        
        layout.addLayout(format_layout)
        
        download_btn = QPushButton('DOWNLOAD', self)
        download_btn.setFont(QFont('Arial', 15, QFont.Bold))
        download_btn.setStyleSheet("background-color: #E74C3C; color: white; padding: 10px; border: 2px solid #E74C3C; border-radius: 15px;")
        download_btn.clicked.connect(self.download_video)
        layout.addWidget(download_btn)
        
        self.setLayout(layout)
        
    def download_video(self):
        link = self.link_input.text()
        format_choice = 'mp4' if self.mp4_radio.isChecked() else 'mp3'
        
        try:
            url = YouTube(link)
            video = url.streams.get_highest_resolution() if format_choice == 'mp4' else url.streams.filter(only_audio=True).first()
            
            options = QFileDialog.Options()
            save_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", f"{format_choice.upper()} files (*.{format_choice});;All Files (*)", options=options)
            
            if save_path:
                video.download(output_path=os.path.dirname(save_path), filename=os.path.basename(save_path))
                if format_choice == 'mp3':
                    base, ext = os.path.splitext(save_path)
                    new_file = base + '.mp3'
                    os.rename(save_path, new_file)
                QMessageBox.information(self, "Success", "Download Complete!")
            else:
                QMessageBox.warning(self, "Error", "No location selected")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to download video: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = YouTubeDownloader()
    ex.show()
    sys.exit(app.exec_())
