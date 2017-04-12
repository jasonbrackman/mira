# -*- coding: utf-8 -*-
import os
import sys
from PySide import QtGui, QtCore
from PySide.phonon import Phonon
from utility.convert_msec import convert_msec
from utility.get_icon_dir import get_icon_dir
from utility.get_conf_data import get_valid_ext
from utility.get_children_files import get_children_files


slider_style_sheet = "QSlider::groove:horizontal{border: 1px solid #165708;" \
                     "background: #8f8f8f;height: 3px;border-radius: 2px;padding-left:-1px;" \
                     "padding-right:-1px;}" \
                     "QSlider::handle:horizontal{border:2px solid #454343;background:#2af5b9;" \
                     "width:9px;margin-top: -4px;margin-bottom: -4px;border-radius: 4px;}" \
                     "QSlider::sub-page:horizontal {background:#2af5b9;border: 1px solid #4A708B;" \
                     "height: 10px;border-radius: 2px;}" \
                     "QSlider::add-page:horizontal {background: #615f5f;border: 0px solid #2af5b9;" \
                     "height: 10px;border-radius: 2px;}"


class PlayerButton(QtGui.QToolButton):
    def __init__(self, name=None, parent=None):
        super(PlayerButton, self).__init__(parent)
        self.__name = name
        # self.setStyleSheet("QToolButton{background-color:transparent;}")
        self.__icon_dir = get_icon_dir()
        icon_path = os.path.join(self.__icon_dir, "%s.png" % self.__name)
        self.setIcon(QtGui.QIcon(icon_path))

    def set_to_pause(self):
        self.setIcon(QtGui.QIcon(os.path.join(self.__icon_dir, "pause.png")))

    def set_to_play(self):
        self.setIcon(QtGui.QIcon(os.path.join(self.__icon_dir, "play.png")))


class VolumeWidget(QtGui.QDialog):
    def __init__(self, parent=None):
        super(VolumeWidget, self).__init__(parent)
        self.setMaximumWidth(15)
        self.setWindowFlags(QtCore.Qt.SplashScreen)
        self.setWindowOpacity(0.8)
        self.setMouseTracking(True)
        main_layout = QtGui.QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.silence_btn = PlayerButton("volume_on", self)
        self.volume_slider = Phonon.VolumeSlider()
        self.volume_slider.setMuteVisible(False)
        self.volume_slider.setFixedHeight(200)
        self.volume_slider.setOrientation(QtCore.Qt.Vertical)
        self.volume_slider.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        main_layout.addWidget(self.silence_btn)
        main_layout.addWidget(self.volume_slider)


class VideoWidget(Phonon.VideoWidget):
    clicked = QtCore.Signal()
    doubleClicked = QtCore.Signal()
    drop = QtCore.Signal(list)

    def __init__(self, parent=None):
        super(VideoWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.valid_ext = get_valid_ext()

    def mouseDoubleClickEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            if self.isFullScreen():
                self.exitFullScreen()
            else:
                self.enterFullScreen()
            self.doubleClicked.emit()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.exitFullScreen()
        if event.key() == QtCore.Qt.Key_Space:
            self.clicked.emit()

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.clicked.emit()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = list()
        for url in event.mimeData().urls():
            path = str(url.toLocalFile())
            children_files = get_children_files(path, self.valid_ext)
            files.extend(children_files)
        files.sort()
        self.drop.emit(files)


class VideoUI(QtGui.QWidget):
    def __init__(self, parent=None):
        super(VideoUI, self).__init__(parent)
        self.__icon_dir = get_icon_dir()
        self.queue = None
        self.__source_files = list()
        self.__count = None
        self.__loop_status = None
        self.__icon_dir = get_icon_dir()
        self.resize(500, 300)
        main_layout = QtGui.QVBoxLayout(self)
        main_layout.setContentsMargins(3, 3, 3, 3)
        main_layout.setSpacing(0)
        self.player = Phonon.MediaObject(self)
        self.player.setTransitionTime(0)
        self.audio_output = Phonon.AudioOutput(Phonon.MusicCategory, self)
        self.audio_output.setVolume(0.5)
        self.current_volume = 0.5
        self.__is_silence = False
        Phonon.createPath(self.player, self.audio_output)
        self.video_widget = VideoWidget(self)
        Phonon.createPath(self.player, self.video_widget)
        self.seek_slider = Phonon.SeekSlider(self.player, self)
        self.seek_slider.setStyleSheet(slider_style_sheet)
        self.seek_slider.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.volume_widget = VolumeWidget(self)
        self.volume_widget.volume_slider.setAudioOutput(self.audio_output)

        btn_layout = QtGui.QHBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(2)
        self.time_label = QtGui.QLabel("00:00:00")
        # self.time_label.setStyleSheet("QLabel{background-color: transparent; color: #AAAAAA}")
        self.total_time_label = QtGui.QLabel("00:00:00")
        # self.total_time_label.setStyleSheet("QLabel{background-color: transparent; color: #AAAAAA}")
        self.stop_btn = PlayerButton("stop", self)
        self.back_btn = PlayerButton("back", self)
        self.play_btn = PlayerButton("play", self)
        self.play_btn.setShortcut("space")
        self.next_btn = PlayerButton("next", self)
        self.full_screen_btn = PlayerButton("full_screen", self)
        self.volume_btn = PlayerButton("volume_on", self)
        self.loop_btn = PlayerButton("loop", self)
        btn_layout.addWidget(self.time_label)
        btn_layout.addWidget(self.seek_slider)
        btn_layout.addWidget(self.total_time_label)
        btn_layout.addWidget(self.stop_btn)
        btn_layout.addWidget(self.back_btn)
        btn_layout.addWidget(self.play_btn)
        btn_layout.addWidget(self.next_btn)
        btn_layout.addWidget(self.full_screen_btn)
        btn_layout.addWidget(self.loop_btn)
        btn_layout.addWidget(self.volume_btn)

        self.loop_menu = QtGui.QMenu()
        self.single_loop_action = QtGui.QAction("Single Loop Play", self)
        self.list_loop_action = QtGui.QAction("List Loop Play", self)
        self.sequential_play_action = QtGui.QAction("Sequential Play", self)
        self.loop_menu.addAction(self.sequential_play_action)
        self.loop_menu.addAction(self.single_loop_action)
        self.loop_menu.addAction(self.list_loop_action)
        self.loop_btn.setMenu(self.loop_menu)

        main_layout.addWidget(self.video_widget)
        main_layout.addLayout(btn_layout)
        self.set_signals()
        self.set_frame_ratio()
        self.loop_none()

        self.silence_icon = QtGui.QIcon(os.path.join(self.__icon_dir, "volume_off.png"))
        self.no_silence_icon = QtGui.QIcon(os.path.join(self.__icon_dir, "volume_on.png"))

    def set_signals(self):
        self.play_btn.clicked.connect(self.switch_play_state)
        self.stop_btn.clicked.connect(self.on_stop)
        self.player.tick.connect(self.show_time)
        self.player.currentSourceChanged.connect(self.reset_total_time)
        self.player.stateChanged.connect(self.on_state_changed)
        self.video_widget.clicked.connect(self.on_widget_clicked)
        self.video_widget.doubleClicked.connect(self.on_widget_clicked)
        self.back_btn.clicked.connect(self.play_back)
        self.next_btn.clicked.connect(self.play_next)
        self.volume_btn.clicked.connect(self.show_volume_slider)
        self.volume_widget.silence_btn.clicked.connect(self.set_silence)
        self.full_screen_btn.clicked.connect(self.set_full_screen)
        self.single_loop_action.triggered.connect(self.loop_single)
        self.list_loop_action.triggered.connect(self.loop_list)
        self.sequential_play_action.triggered.connect(self.loop_none)

    def set_frame_ratio(self, ratio=24):
        self.player.setTickInterval(1000/ratio)
        self.seek_slider.setSingleStep(1000/ratio)
        self.player.setPrefinishMark(1000/ratio)

    def switch_play_state(self):
        if self.player.state() in [Phonon.PausedState, Phonon.LoadingState, Phonon.StoppedState]:
            self.on_play()
        elif self.player.state() in [Phonon.PlayingState]:
            self.on_pause()

    def on_play(self):
        self.play_btn.set_to_pause()
        self.player.play()

    def play_when_loop(self):
        self.on_play()
        if self.__loop_status == "list":
            self.loop_list()
        elif self.__loop_status == "single":
            self.loop_single()

    def on_stop(self):
        self.play_btn.set_to_play()
        self.player.stop()

    def on_pause(self):
        self.play_btn.set_to_play()
        self.player.pause()

    def show_volume_slider(self):
        if self.__is_silence:
            if not self.volume_widget.isHidden():
                self.volume_widget.hide()
            else:
                self.volume_btn.setIcon(self.no_silence_icon)
                self.volume_widget.silence_btn.setIcon(self.no_silence_icon)
                self.audio_output.setVolume(self.current_volume)
                self.__is_silence = False
        else:
            if self.volume_widget.isHidden():
                self.volume_widget.show()
                self.volume_widget_move()
            else:
                self.volume_widget.hide()

    def volume_widget_move(self):
        if not self.volume_widget.isHidden():
            volume_btn_pos = self.mapToGlobal(self.volume_btn.pos())
            self.volume_widget.move(volume_btn_pos.x(), volume_btn_pos.y()-self.volume_widget.height())

    def set_silence(self):
        if self.__is_silence:
            self.volume_widget.silence_btn.setIcon(self.no_silence_icon)
            self.volume_btn.setIcon(self.no_silence_icon)
            self.audio_output.setVolume(self.current_volume)
            self.__is_silence = False
        else:
            self.current_volume = self.audio_output.volume()
            self.volume_widget.silence_btn.setIcon(self.silence_icon)
            self.volume_btn.setIcon(self.silence_icon)
            self.audio_output.setVolume(0)
            self.volume_widget.hide()
            self.__is_silence = True

    def set_source(self, source):
        self.loop_none()
        if isinstance(source, basestring):
            source = [source]
        source = [i.replace("\\", "/") for i in source]
        self.__source_files = source
        self.queue = list()
        for i in source:
            source_object = Phonon.MediaSource(i)
            source_object.Type = 0
            self.queue.append(source_object)
        self.player.clear()
        self.player.enqueue(self.queue)
        self.on_play()
        # if delete current, stop current and restart
        current_source = self.player.currentSource()
        if not current_source:
            return
        if current_source.fileName() not in self.__source_files:
            self.player.stop()

    def show_time(self):
        current_time = self.player.currentTime()
        date_time = convert_msec(current_time)
        self.time_label.setText(date_time)

    def reset_total_time(self):
        total_time = self.player.totalTime()
        date_time = convert_msec(total_time)
        self.total_time_label.setText(date_time)

    def on_state_changed(self, new_state, old_state):
        if old_state in [Phonon.LoadingState] and new_state == Phonon.PlayingState:
            self.reset_total_time()

    def on_widget_clicked(self):
        if self.player.state() == Phonon.PlayingState:
            self.on_pause()
            self.play_btn.set_to_play()
        elif self.player.state() == Phonon.PausedState:
            self.on_play()
            self.play_btn.set_to_pause()
        if not self.volume_widget.isHidden():
            self.volume_widget.hide()

    # def set_background(self):
    #     self.image = QtGui.QImage()
    #     self.image.load(r'D:/picture/bg.jpg')
    #     self.setAutoFillBackground(True)
    #     palette = QtGui.QPalette()
    #     palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(
    #         self.image.scaled(self.width(), self.height(),
    #                           QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)))
    #     self.setPalette(palette)
    #
    # def resizeEvent(self, event):
    #     palette = QtGui.QPalette()
    #     palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(
    #         self.image.scaled(event.size(), QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)))
    #     self.setPalette(palette)

    def set_full_screen(self, value=True):
        self.video_widget.setFullScreen(value)

    def play_back(self):
        current_source = self.player.currentSource()
        current_file = current_source.fileName()
        if not current_file:
            return
        current_index = self.__source_files.index(current_file)
        if current_index == 0:
            self.player.setCurrentSource(current_source)
            self.on_play()
        else:
            last_index = current_index - 1
            self.player.setCurrentSource(self.queue[last_index])
            self.on_play()
        if self.__loop_status == "list":
            self.loop_list()
        elif self.__loop_status == "single":
            self.loop_single()

    def play_next(self):
        current_source = self.player.currentSource()
        current_file = current_source.fileName()
        if not current_file:
            return
        current_index = self.__source_files.index(current_file)
        if current_index == len(self.queue) - 1:
            self.player.setCurrentSource(current_source)
            self.on_play()
        else:
            next_index = current_index + 1
            self.player.setCurrentSource(self.queue[next_index])
            self.on_play()
        if self.__loop_status == "list":
            self.loop_list()
        elif self.__loop_status == "single":
            self.loop_single()

    def loop_list(self):
        self.__loop_status = "list"
        self.single_loop_action.setIcon(QtGui.QIcon(""))
        self.sequential_play_action.setIcon(QtGui.QIcon(""))
        self.list_loop_action.setIcon(QtGui.QIcon(os.path.join(self.__icon_dir, "selected.png")))
        self.player.prefinishMarkReached.connect(self.set_loop)

    def loop_single(self):
        self.__loop_status = "single"
        self.list_loop_action.setIcon(QtGui.QIcon(""))
        self.sequential_play_action.setIcon(QtGui.QIcon(""))
        self.single_loop_action.setIcon(QtGui.QIcon(os.path.join(self.__icon_dir, "selected.png")))
        current_source = self.player.currentSource()
        if not current_source.fileName():
            return
        self.player.setQueue([current_source])
        self.player.prefinishMarkReached.connect(self.set_loop)
        state = self.player.state()
        if state in [Phonon.PausedState, Phonon.StoppedState]:
            self.player.seek(0)
        self.on_play()

    def set_loop(self):
        if self.__loop_status == "list":
            if self.queue:
                self.player.clear()
                self.player.enqueue(self.queue)
                self.on_play()
        elif self.__loop_status == "single":
            current_source = self.player.currentSource()
            self.player.clear()
            self.player.enqueue([current_source])
            self.player.seek(0)
            self.on_play()

    def loop_none(self):
        self.__loop_status = None
        self.single_loop_action.setIcon(QtGui.QIcon(""))
        self.list_loop_action.setIcon(QtGui.QIcon(""))
        self.sequential_play_action.setIcon(QtGui.QIcon(os.path.join(self.__icon_dir, "selected.png")))
