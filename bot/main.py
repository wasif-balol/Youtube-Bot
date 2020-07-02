import os
import sys
import time

from PIL import Image, ImageDraw, ImageFont

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QLabel, QMessageBox, QPushButton, QPlainTextEdit, QLineEdit
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from collections import deque

executable_path = "chromedriver.exe"
os.environ["webdriver.chrome.driver"] = executable_path
option = Options()
option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("disable-popup-blocking")
# option.add_argument("--headless")
option.add_argument("--mute-audio")
option.add_argument("--disable-popup-blocking")

class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(320, 340))
        self.setWindowTitle("Application")
        self.setMaximumSize(QSize(320, 340))

        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Link/Links:')
        self.nameLabel.setFont(QtGui.QFont("Times", 11, QtGui.QFont.Bold))
        self.link = QPlainTextEdit(self)
        self.link.setPlaceholderText("One link per line")

        self.link.move(90, 5)
        self.link.resize(200, 52)
        self.nameLabel.move(11, 10)

        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Seconds:')
        self.nameLabel.setFont(QtGui.QFont("Times", 11, QtGui.QFont.Bold))
        self.duration = QPlainTextEdit(self)
        self.duration.setPlaceholderText("Enter Duration in Seconds")

        self.duration.move(90, 70)
        self.duration.resize(200, 52)
        self.nameLabel.move(11, 80)

        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Title/Titles:')
        self.nameLabel.setFont(QtGui.QFont("Times", 11, QtGui.QFont.Bold))
        self.title = QPlainTextEdit(self)

        self.title.move(90, 135)
        self.title.resize(200, 52)
        self.nameLabel.move(11, 140)
        self.title.setPlaceholderText("One title per line")

        self.yearLabel = QLabel(self)
        self.yearLabel.setText('Year:')
        self.yearLabel.setFont(QtGui.QFont("Times", 11, QtGui.QFont.Bold))
        self.year = QPlainTextEdit(self)

        self.year.move(90, 200)
        self.year.resize(200, 52)
        self.yearLabel.move(30, 205)
        self.year.setPlaceholderText("One year per line")

        pybutton = QPushButton('OK', self)
        pybutton.clicked.connect(self.clickMethod)
        pybutton.resize(240, 62)
        pybutton.move(40, 260)

    def show_message(self, string):
        msg = QMessageBox(self)
        msg.about(self, "Message", string)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    def clickMethod(self):
        links = self.link.toPlainText().split('\n')
        titles = self.title.toPlainText().split('\n')
        titles = [str(i)[::-1] for i in titles]

        titles = [''.join(deque(i)) for i in titles]
        year = self.year.toPlainText().split('\n')
        duration = self.duration.toPlainText()
        if (duration == ''):
            self.show_message("Fill the form correctly")
            return
        if (links[0] == '') | (titles[0] == '') | (year[0] == ''):
            self.show_message("File the form correctly")
            self.title.clear()
            self.link.clear()
            self.duration.clear()
            self.year.clear()
            return
        if len(links) != len(titles) != len(year):
            self.show_message("links, titles and years lengths are not equal")
            self.title.clear()
            self.link.clear()
            self.duration.clear()
            self.year.clear()
            return
        self.show_message("Form is valid Press Ok to continue")
        self.run(links, duration.strip(), titles, year)

    def run(self, links, seconds, titles, year):
        try:
            current_dir = os.getcwd()
            path = os.path.join(current_dir, 'pictures')
            os.mkdir(path)
        except OSError as error:
            pass
        driver = webdriver.Chrome(executable_path=executable_path, options=option)

        for link, title, year in zip(links, titles, year):
            try:
                driver.get(link.strip())
                time.sleep(3)
                try:
                    driver.find_element_by_class_name('ytp-ad-skip-button').click()
                    time.sleep(2)
                except:
                    pass
                playing_status = \
                    driver.find_element_by_class_name('ytp-play-button').get_attribute('aria-label').split(' ')[0]

                if playing_status == "Play":
                    driver.find_element_by_class_name('ytp-play-button').click()
                    time.sleep(4)
                try:
                    time.sleep(2)
                    driver.find_element_by_class_name('ytp-ad-skip-button').click()
                    time.sleep(2)
                except:
                    pass
                try:
                    driver.find_element_by_class_name('ytp-ad-preview-container')
                    time.sleep(1)
                    driver.find_element_by_class_name('ytp-ad-skip-button').click()
                    time.sleep(2)
                except:
                    pass
                time.sleep(5)
                driver.find_element_by_class_name('ytp-play-button').click()
                driver.execute_script('document.getElementsByTagName("video")[0].currentTime = 0')
                driver.execute_script('document.getElementsByTagName("video")[0].currentTime += {}'.format(seconds))
                time.sleep(3)
                try:
                    overlay = driver.find_element_by_class_name('ytp-ad-overlay-close-button')
                    overlay.click()
                except Exception as e:
                    pass
                time.sleep(1)

                element = driver.find_element_by_class_name('html5-main-video')

                try:
                    driver.execute_script(
                        "document.getElementsByClassName('ytp-ad-overlay-slot')[0].setAttribute('hidden','')")
                except Exception as e:
                    print(e.__str__())
                    pass

                location = element.location
                size = element.size

                try:
                    driver.execute_script(
                        "document.getElementsByClassName('ytp-cards-button-icon')[0].setAttribute('hidden','')")
                except:
                    pass
                try:
                    driver.execute_script(
                        "document.getElementsByClassName('ytp-ad-text-overlay')[0].setAttribute('hidden','')")
                except:
                    pass
                try:
                    driver.execute_script(
                        "document.getElementsByClassName('ytp-cards-teaser')[0].setAttribute('hidden','')")
                except:
                    pass

                try:
                    driver.execute_script(
                        "document.getElementsByClassName('ytd-popup-container')[0].setAttribute('hidden','')")
                except:
                    pass
                try:
                    driver.execute_script(
                        "document.getElementsByClassName('ytd-mealbar-promo-renderer')[0].setAttribute('hidden','')")
                except:
                    pass

                driver.execute_script("document.getElementsByClassName('ytp-title')[0].setAttribute('hidden','')")
                driver.execute_script(
                    "document.getElementsByClassName('ytp-chrome-bottom')[0].setAttribute('hidden','')")
                file_name = (str(title)[::-1].replace(' ', '_') + "_" + str(year) + '.jpg')
                driver.save_screenshot("pictures\{}".format(file_name))
                x = location['x']
                y = location['y']
                width = location['x'] + size['width']
                height = location['y'] + size['height']
                im = Image.open("pictures\{}".format(file_name))
                im = im.crop((int(x), int(y), int(width - 2), int(height)))

                im = im.convert('RGB')
                im.save("pictures\{}".format(file_name))
                width, height = im.size
                create_image(file_name, im, title, height, width, year)
            except Exception as e:
                print(e.__str__())
                pass

        self.show_message("Screenshot taken from all links press ok to close")
        driver.close()
        mainWin.close()


def create_image(file, imagee, title, height, width, year):
    fnt = ImageFont.truetype('FontsFree-Net-arial-bold.ttf', 31)
    new_image = Image.new(mode="RGB", size=(width + fnt.getsize(title)[0] + 50, height), color="red")
    draw = ImageDraw.Draw(new_image)

    size = (fnt.getsize(title)[0]) / 2
    year_length = (fnt.getsize(year)[0]) / 2
    draw.text(((width + ((new_image.size[0] - width) / 2) - size), height / 2.3), str(title.replace('_', ' ')),
              font=fnt, fill=(255, 255, 255))
    draw.text(((width + ((new_image.size[0] - width) / 2) - year_length), height / 1.9), str(year), font=fnt,
              fill=(255, 255, 255))
    new_image.paste(imagee, (0, 0))
    new_image.save("pictures\{}".format(file))
    return True



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())

# try:
#     driver.execute_script(
#         "document.getElementsByClassName('ytp-ad-overlay-image')[0].setAttribute('hidden','')")
# except:
#     pass
# try:
#     driver.execute_script(
#         "document.getElementsByClassName('ytp-ad-overlay-ad-info-button-container')[0].setAttribute('hidden','')")
# except:
#     pass
#
# try:
#     driver.execute_script(
#         "document.getElementsByClassName('ytp-ad-overlay-close-button')[0].setAttribute('hidden','')")
# except Exception as e:
#     pass
# try:
#     driver.execute_script(
#         "document.getElementsByClassName('ytp-ad-overlay-close-container')[0].setAttribute('hidden','')")
# except Exception as e:
#     pass
# try:
#     driver.execute_script(
#         "document.getElementsByClassName('ytp-ad-hover-text-button')[0].setAttribute('hidden','')")
# except:
#     pass

# try:
#     driver.execute_script(
#         "document.getElementsByClassName('ytp-ad-hover-close-button')[0].setAttribute('hidden','')")
# except Exception as e:
#     print(e.__str__())
#     pass
# try:
#     driver.execute_script(
#         "document.getElementsByClassName('ytp-ad-info-hover-text-button')[0].setAttribute('hidden','')")
# except:
#     pass
