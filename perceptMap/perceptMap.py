from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, ListProperty, BooleanProperty, DictProperty
from kivy.graphics import Color, Line
from kivy.uix.stencilview import StencilView
from kivy.uix.slider import Slider
# from threading import Thread
from kivy.uix.accordion import Accordion
from kivy.uix.popup import Popup
import yaml
import os


class UserResponse(BoxLayout):
    """Main Kivy app class

    Contains the root widget that is updated after every user interaction, along with methods to save and reset the GUI.
    This app can also be run in auto-mode where file save and resset can be triggered by an external command. Pseudocode
    to set this up is included.
    """

    rootPath = StringProperty()
    repNumber = NumericProperty(0)
    sensationNumber = NumericProperty(0)
    saveFolder = StringProperty('default')
    responseAnnot = set()

    def __init__(self, inputroot, imgfiles, tablabels, lastRep, mmm_ip, **kwargs):
        """
        Parameters
        ----------
        inputroot : str
            filepath where output files will be saved
        imgfiles:
            list of pngs to use for tabbed panel canvas
        tablabels:
            labels for tabs describing image
        lastRep:
            counter for the last trial
        mmm_ip : str
            IP address of message server machine (if using auto-mode)
        """

        super(UserResponse, self).__init__(**kwargs)
        self.rootPath = inputroot
        self.imgfiles = imgfiles
        self.repNumber = lastRep
        for idx, tabImg in enumerate(zip(imgfiles, tablabels)):
            self.ids['img%d' % idx].source = '../ImageBank/%s.png' % tabImg[0]
            self.ids['img%d' % idx].imglabel = tabImg[0]
            self.ids['tab%d' % idx].text = tabImg[1]

        # PLACEHOLDER: connect to message server, subscribe to messages
        # PLACEHOLDER: start listener thread
        # self.listener=Thread(target=self.pyConsumer)
        # self.listener.daemon=True
        # self.listener.start()
        # print ("Consumer running...\n")

    def save_data(self):
        """Saves radiobutton, checkbox and slider values entered by user to a yml file in the specified location"""

        self.ids['responseAcc'].copy_accordion()

        fname = os.path.join(self.rootPath, self.saveFolder, self.saveFolder+"_R%03d" % self.repNumber)
        radiosliderdict = self.ids['responseAcc'].labelCheckDict.copy()
        sensationdict = self.ids['floatStencilArea'].lineDict.copy()
        movedirdict = self.ids['floatStencilArea'].moveDict.copy()
        imgpropertiesdict = {'size': list(self.ids['img0'].get_norm_image_size()), 'pos': list(self.ids['img0'].pos)}

        if sensationdict or radiosliderdict['Sensation0']:
            if not (self.saveFolder in self.responseAnnot):
                self.responseAnnot.add(self.saveFolder)

            if not os.path.exists(os.path.join(self.rootPath, self.saveFolder)):
                    os.makedirs(os.path.join(self.rootPath, self.saveFolder))

            if sensationdict:
                with open(fname+'_imPixel.yml', 'w') as outfile:
                    outfile.write(yaml.dump(imgpropertiesdict, default_flow_style=False))
                    outfile.write(yaml.dump(sensationdict, default_flow_style=False))
                self.ids['floatStencilArea'].lineDict.clear()

            if movedirdict:
                with open(fname+'_dirPixel.yml', 'w') as outfile:
                    outfile.write(yaml.dump(imgpropertiesdict, default_flow_style=False))
                    outfile.write(yaml.dump(movedirdict, default_flow_style=False))
                    self.ids['floatStencilArea'].moveDict.clear()

            if radiosliderdict['Sensation0']:
                with open(fname+'_RadioCheckSlider.yml', 'w') as outfile:
                    outfile.write(yaml.dump(radiosliderdict, default_flow_style=False))
                    self.ids['responseAcc'].labelCheckDict.clear()

    def clear_window_canvas(self):
        """Clears all drawn lines on the image canvas"""

        for idx in range(len(self.imgfiles)):
            self.ids['img%d' % idx].clear_drawn_lines('all')

    def reset_radio_check_slider(self):
        """resets radiobutton, checkbox and slider values"""

        self.ids['qualityAccordion'].collapse = False
        self.ids['modalityAccordion'].collapse = True
        self.ids['mechBox'].set_labels_and_radio(False)
        self.ids['tingleBox'].set_labels_and_radio(False)
        self.ids['tempBox'].set_labels_and_radio(False)
        self.ids['moveBox'].set_labels_and_radio(False)
        for i in self.ids['depthBox1'].children:
            i.active = False
        for i in self.ids['depthBox2'].children:
            i.active = False
        self.ids['naturalSlider'].value = 0         # this is possibly redundant with the set_labels_and_radio method
        self.ids['naturalSlider'].cursor_image = '../ImageBank/sliderVal.png'
        self.ids['painSlider'].value = 0
        self.ids['painSlider'].cursor_image = '../ImageBank/sliderVal.png'
        self.ids['phantomSlider'].value = 0
        self.ids['phantomSlider'].cursor_image = '../ImageBank/sliderVal.png'
        self.ids['tempSlider'].value = 0

        pass

    # PLACEHOLDER: listener function
    # def pyConsumer(self):
    #    """Runs an infinite while loop to listen to subscribed messages and trigger GUI events when run in auto-mode"""
    #     disableScreen=Popup(opacity = 0.8, auto_dismiss = False, title = 'RESPONSES DISABLED', title_align = 'center')
    #     disableScreen.open()
    #     time.sleep(0.5)
    #
    #     while (1):
    #         non-blocking read of every subscribed message
    #         if TRIAL_START
    #               set self.saveFolder name
    #               reset counters
    #               disable popup
    #               play tone
    #
    #         elif STIM_END
    #               dismiss popup/enable GUI
    #
    #         elif TRIAL_END
    #             self.save_data()
    #             Clock.schedule_once(lambda dt: self.ids["imageTab"].switch_to(self.ids["imageTab"]._original_tab))
    #             Clock.schedule_once(lambda dt: self.clear_window_canvas())
    #             Clock.schedule_once(lambda dt: self.reset_radio_check_slider())
    #             Clock.schedule_once(lambda dt: disableScreen.open())
    #
    #         time.sleep(0.001)
    #     pass


class SaveResetButton(Button):
    """Triggers file save and GUI reset when GUI is run in manual-mode

    comment this class if running in auto mode
    """

    def __init__(self, **kwargs):
        super(SaveResetButton, self).__init__(**kwargs)

    def on_press(self):
        """Button callback to save data and reset GUI"""

        rootwidget = self.get_root_window().children[-1]
        stencilobj = self.get_root_window().children[-1].ids['floatStencilArea']
        rootwidget.save_data()
        rootwidget.clear_window_canvas()
        rootwidget.reset_radio_check_slider()
        rootwidget.repNumber += 1
        rootwidget.sensationNumber = 0
        rootwidget.ids["imageTab"].switch_to(rootwidget.ids["imageTab"]._original_tab)
        # prevent propagation of touch
        stencilobj.buttonPress = True
        return True


class ResponseAccordion(Accordion):
    """Accordion containing descriptors for quality and modality

    """

    tempDict = DictProperty({})               # flushed after each sensation
    labelCheckDict = DictProperty({})

    def __init__(self, **kwargs):
        super(ResponseAccordion, self).__init__(**kwargs)

    def copy_accordion(self):
        """copies user responses from widget to temporary dictionary

        """

        sensekey = 'Sensation'+str(self.get_parent_window().children[-1].sensationNumber)
        responseaccobj = self.get_parent_window().children[-1].ids['responseAcc']

        responseaccobj.labelCheckDict[sensekey] = responseaccobj.tempDict.copy()
        responseaccobj.tempDict.clear()


class LabelCheckResponse(CheckBox, Label):
    """class for checkbox/radio button with associated text

    """

    def __init__(self, **kwargs):
        super(LabelCheckResponse, self).__init__(**kwargs)

    def on_touch_up(self, touch):
        """enables checkbox/radiobutton

        """

        if touch.grab_current == self:
            self.set_labels_and_radio(self.active)

    def set_labels_and_radio(self, isactive):
        """callback for radio or checkbox

        """

        rootwidget = self.get_root_window().children[-1]
        if isactive:  # is active
            if not self.group:  # checkbox
                for responseObj in self.parent.children[:-1]:
                    responseObj.canvas.opacity = 1              # canvas of boxlayout
                    responseObj.disabled = False

                print(self.text + ' enabled: ' + str(self.active))

            else:  # radiobox
                if self.active:  # 2 radio selections are detected as active. can be handled better by binding on_active
                    rootwidget.ids['responseAcc'].tempDict[self.group] = self.text
                    print(self.group + ' - ' + self.text + ' sensation')

                    if self.group == 'movement' and self.text != "Vibration":
                            popup = MovementPopup()
                            popup.open()

                    # PLACEHOLDER: send message for selected radiobutton

        else:  # is inactive
            if not self.group:          # checkbox
                self.active = False
                if self.text == 'Temperature':
                    rootwidget.ids['tempBox'].parent.children[0].children[1].value = 0
                    rootwidget.ids['tempBox'].parent.children[0].children[1].cursor_image = '../ImageBank/sliderVal.png'
                    rootwidget.ids['tempBox'].parent.children[0].canvas.opacity = 0.5
                    rootwidget.ids['tempBox'].parent.children[0].disabled = True
                else:

                    for responseObj in self.parent.children[:-1]:
                        responseObj.canvas.opacity = 0.5   # canvas of boxlayout
                        responseObj.disabled = True

                    for radioObj in self.parent.children[1].children:
                            radioObj.active = False

                    self.parent.children[0].children[1].value = 0   # slider
                    self.parent.children[0].children[1].cursor_image = '../ImageBank/sliderVal.png'

                    if self.group in rootwidget.ids['responseAcc'].tempDict.keys():
                        rootwidget.ids['responseAcc'].tempDict[self.group] = ''


class SliderResponse(Slider):
    """class for all slider/intensity widgets

    """
    id = ObjectProperty(None)
    id2 = StringProperty('')

    def __init__(self, **kwargs):
        super(SliderResponse, self).__init__(**kwargs)
        self.cursor_image = '../ImageBank/sliderVal.png'

    def on_touch_up(self, touch):
        rootwidget = self.get_root_window().children[0]
        if touch.grab_current == self:
            self.cursor_image = 'atlas://data/images/defaulttheme/slider_cursor'
            self.value_pos = touch.pos
            rootwidget.ids['responseAcc'].tempDict[self.id2] = round(self.value, 3)
            print(self.value)

            # PLACEHOLDER: send message for slider value


class MovementPopup(Popup):
    """popup to draw movement direction

    this popup is enabled iff the movement checkbox is selected and any radiobutton other than vibration is selected
    """

    def __init__(self, **kwargs):
        super(MovementPopup, self).__init__(**kwargs)
        content = BoxLayout(orientation='vertical')
        content.add_widget(MovementCanvas(text="Draw Here", font_size=20, size_hint_y=0.9))
        mybutton = MovementButton(text="Finished Entering Direction", size_hint=(1, 0.1), font_size=20)
        content.add_widget(mybutton)

        self.canvas.opacity = 0.3
        self.background_color = 1, 1, 1, 1
        self.content = content
        self.title = 'Draw Movement Direction'
        self.auto_dismiss = False
        self.size_hint = (.55, 1)
        self.pos_hint = {'right': 0.95, 'y': 0}
        self.font_size = 20

        mybutton.bind(on_press=self.close_popup)

    def close_popup(self, instance):
        self.dismiss()


class MovementCanvas(Label):
    """canvas to draw movement direction within MovemenPopup widget

    """

    def __init__(self, **kwargs):
        super(MovementCanvas, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):        # collides with label area
            with self.canvas:
                Color(0, 0, 0)
                touch.ud['line'] = Line(width=5, points=(touch.x, touch.y))
            return True

    def on_touch_move(self, touch):
        if self.collide_point(touch.x, touch.y) and 'line' in touch.ud.keys():
            touch.ud['line'].points += [touch.x, touch.y]
            return True

        else:
            return True

    def on_touch_up(self, touch):
        rootwidget = self.get_parent_window().children[-1]
        stencilobj = rootwidget.ids['floatStencilArea']
        imageobj = rootwidget.ids[stencilobj.currImage]
        sensekey = 'sensation'+str(rootwidget.sensationNumber)+'_'+stencilobj.currImagename

        if self.collide_point(touch.x, touch.y):
            if 'line' in touch.ud.keys():
                stencilobj.moveDict[sensekey] = touch.ud['line'].points
                with imageobj.canvas:
                    imageobj.segment_color.append(Color(*imageobj.colors[int(rootwidget.sensationNumber % 13)]))
                    Line(points=touch.ud['line'].points, width=5)

                # PLACEHOLDER: send message with pixel coordinates

                return True

            else:
                return True
        else:
            return True


class MovementButton(Button):
    """Button within movement popup

    press button to indicate user is finished entering movement direction
    """

    def __init__(self, **kwargs):
        super(MovementButton, self).__init__(**kwargs)

    def on_press(self):
        stencilobj = self.get_root_window().children[1].ids['floatStencilArea']

        # if a line has not been drawn on the canvas before a movement is added then the currImage is not updated
        if not(stencilobj.currImage == self.get_root_window().children[1].ids['imageTab'].current_tab.content.id2):
            stencilobj.currImage = self.get_root_window().children[1].ids['imageTab'].current_tab.content.id2

        imageobj = self.get_root_window().children[1].ids[stencilobj.currImage]
        imageobj.save_png(1)


class SensationButton(Button):
    """2 rectangular buttons in bottom right corner

    all lines that are drawn on the current image are cleared when the clear button is pressed. when add sensation
    button is pressed, opacity of all lines is changed, these lines cannot be edited or cleared and the counter
    for sensation is incremented
    """

    id2 = StringProperty('')

    def __init__(self, **kwargs):
        super(SensationButton, self).__init__(**kwargs)

    def on_press(self):

        rootwidget = self.get_root_window().children[-1]
        responseaccobj = self.get_parent_window().children[-1].ids['responseAcc']
        stencilobj = self.get_root_window().children[-1].ids['floatStencilArea']

        if self.id2 == 'add':

            # copy current dictionary to accordion dictionary
            responseaccobj.copy_accordion()

            # set new color
            rootwidget.ids['imageTab'].children[1].children[0].paintbrush()

            # clear pointers to line objects from previous sensation
            rootwidget.ids['imageTab'].children[1].children[0].oldSegment_buffer.extend(rootwidget.ids['imageTab'].children[1].children[0].segment_color)
            rootwidget.ids['imageTab'].children[1].children[0].segment_color = []

            # clear all radio buttons
            self.get_parent_window().children[-1].reset_radio_check_slider()

            print('added sensation')

        else:  # clear lines button

            sensekey = 'sensation'+str(rootwidget.sensationNumber)+'_'+stencilobj.currImagename

            if sensekey in stencilobj.lineDict.keys():        # line has been drawn

                del stencilobj.lineDict[sensekey]       # delete pixel coordinates

                rootwidget.ids[stencilobj.currImage].clear_drawn_lines('currentSense')

            if sensekey in stencilobj.moveDict.keys():
                stencilobj.moveDict[sensekey] = []

            # rootwidget.reset_radio_check_slider()

        # prevent propagation of touch
        stencilobj.buttonPress = True
        return True


class FloatStencil(FloatLayout, StencilView):
    """Widget containing tabbed panel items and png images

    """

    lineDict = DictProperty()
    moveDict = DictProperty()
    buttonPress = BooleanProperty(False)
    currImage = StringProperty('img0')
    currImagename = StringProperty('')

    def __init__(self, **kwargs):
        super(FloatStencil, self).__init__(**kwargs)


class CustomImage(Image):
    """widget containing png images

    all lines are drawn on the canvas of this widget. Lines drawn in the movement popup are transferred to this canvas.
    The color of the line is based on the sensation number. The order of colors is stored in self.colors property. The
    default order of line colors is purple, cyan, green, red, blue, yellow, orange, pink, brown, aqua-green, magenta,
    orange-chalk, teal
    """

    colors = ListProperty()

    oldSegment_buffer = ListProperty()
    segment_color = ListProperty()
    moveSegment_color = ListProperty()
    id2 = StringProperty('')

    def __init__(self, **kwargs):
        super(CustomImage, self).__init__(**kwargs)
        self.colors = [[0.5, 0.00, 0.8], [0.16, 0.78, 0.88], [0.31, 0.63, 0.06], [0.95, 0.37, 0.39], [0.35, 0.35, 0.82],
                       [0.99, 0.90, 0.05], [0.93, 0.54, 0.14], [0.93, 0.24, 0.89], [0.64, 0.38, 0.00],
                       [0.12, 0.74, 0.48], [0.93, 0.18, 0.55], [0.98, 0.45, 0.37], [0.09, 0.22, 0.25]]

    def paintbrush(self):
        with self.canvas:
            for lineObj in self.segment_color:
                lineObj.a = 0.5
            self.get_parent_window().children[-1].sensationNumber += int(1)

    def on_touch_down(self, touch):

        stencilobj = self.get_root_window().children[-1].ids['floatStencilArea']

        if self.collide_point(touch.x, touch.y):
            stencilobj.currImage = self.id2
            stencilobj.currImagename = self.imglabel
            stencilobj.buttonPress = False
            with self.canvas:
                self.segment_color.append(Color(*self.colors[int(self.get_parent_window().children[-1].sensationNumber % 13)]))
                touch.ud['line'] = Line(width=5, points=(touch.x, touch.y))
            return True

    def on_touch_move(self, touch):
        stencilobj = self.get_root_window().children[-1].ids['floatStencilArea']

        if not stencilobj.buttonPress:
            if self.collide_point(touch.x, touch.y) and 'line' in touch.ud.keys():
                touch.ud['line'].points += [touch.x, touch.y]
                return True

    def on_touch_up(self, touch):

        stencilobj = self.get_root_window().children[-1].ids['floatStencilArea']

        if not stencilobj.buttonPress:
            if self.collide_point(touch.x, touch.y):
                if 'line' in touch.ud.keys():

                    currentimg = stencilobj.currImagename
                    sensekey = 'sensation'+str(self.get_parent_window().children[-1].sensationNumber)+'_'+currentimg

                    if sensekey in stencilobj.lineDict.keys():
                        stencilobj.lineDict[sensekey] += touch.ud['line'].points
                    else:
                        stencilobj.lineDict[sensekey] = touch.ud['line'].points

                    self.save_png(0)

                    # PLACEHOLDER: send message with pixel coordinates
                    return True

                else:
                    return True

        else:
            stencilobj.buttonPress = False
            return True

    def clear_drawn_lines(self, lines):
        if lines == 'currentSense':               # clear latest drawn line.
            with self.canvas:
                for lineObj in self.segment_color:
                    lineObj.a = 0
            self.segment_color = []
        else:                                   # clear all lines
            with self.canvas:
                for lineObj in self.segment_color + self.oldSegment_buffer:
                    lineObj.a = 0
            self.segment_color = []

    def save_png(self, child_idx):
        rootwidget = self.get_parent_window().children[child_idx]
        if not os.path.exists(os.path.join(rootwidget.rootPath, rootwidget.saveFolder)):
            os.makedirs(os.path.join(rootwidget.rootPath, rootwidget.saveFolder))

        self.export_to_png(os.path.join(rootwidget.rootPath, rootwidget.saveFolder,
                                        rootwidget.saveFolder+"_R%03d" % rootwidget.repNumber+'_'+self.imglabel+'.png'))


class PerceptMap(App):
    """perceptmap app class

    if a perceptmap.ini file does not exist it will be created in the same folder with the dfault parameters specified in
    build_config. edit the *.ini file to change these parameters
    """

    def build_config(self, config):
        config.setdefaults('config', {
            'savePath': '../data',
            'mmip': 'localhost',
            'windowSize': (1368, 912),
            'windowColor': (1, 1, 1, 1),
            'windowBorderless': False,
            'imgFiles': ['Rpalmar', 'Rdorsum', 'Farms', 'Barms', 'Lpalmar', 'Ldorsum'],
            'tabLabels': ['Right\nPalm', 'Right\nDorsum', 'Arms\nFront', 'Arms\nBack', 'Left\nPalm', 'Left\nDorsum'],
            'trialNumber': 0
        })

    def build(self):
        config = self.config
        Window.size = eval(config.get('config', 'windowSize'))
        Window.clearcolor = eval(config.get('config', 'windowColor'))
        Window.borderless = config.getboolean('config', 'windowBorderless')
        if not os.path.exists(config.get('config', 'savePath')):
            os.makedirs(config.get('config', 'savePath'))
        return UserResponse(config.get('config', 'savePath'), eval(config.get('config', 'imgFiles')),
                            eval(config.get('config', 'tabLabels')), int(config.get('config', 'trialNumber')),
                            config.get('config', 'mmip'))

    def on_stop(self):
        config = self.config
        config.set('config', 'trialNumber', self.root_window.children[-1].repNumber)
        config.write()


if __name__ == '__main__':
    PerceptMap().run()
