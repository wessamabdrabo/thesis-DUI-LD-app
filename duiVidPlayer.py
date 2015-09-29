# install_twisted_rector must be called before importing  and using the reactor
import plistlib
from kivy.support import install_twisted_reactor
install_twisted_reactor()


from twisted.internet import reactor
from twisted.internet import protocol

class TCPServerProtocol(protocol.Protocol):
    def dataReceived(self, data):
        response = self.factory.app.handle_message(data)
        #if response:
        #    self.transport.write(response)


class TCPServerFactory(protocol.Factory):
    protocol = TCPServerProtocol

    def __init__(self, app):
        self.app = app

import kivy
kivy.require('1.0.5')
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.image import AsyncImage

class DetailWidget(FloatLayout):
    title = StringProperty('')
    imageURL = StringProperty('')
    speaker = StringProperty('')
    duration = StringProperty('')
    descr = StringProperty('')
    pass

class FilterWidget(BoxLayout):
    title = StringProperty('')
    imageURL = StringProperty('')
    pass


class DUIVidPlayer(FloatLayout):    
    def __init__(self, vids, **kwargs):
        super(DUIVidPlayer, self).__init__(**kwargs)
        print "in DUIVidPlayer"

        self.ids.img1.source = vids[19]['imgUrl']
        self.ids.title1.text = vids[19]['title']

        self.ids.img2.source = vids[8]['imgUrl']
        self.ids.title2.text = vids[8]['title']

        self.ids.img3.source = vids[70]['imgUrl']
        self.ids.title3.text = vids[70]['title']

        self.ids.img4.source = vids[57]['imgUrl']
        self.ids.title4.text = vids[57]['title']

        self.ids.img5.source = vids[56]['imgUrl']
        self.ids.title5.text = vids[56]['title']
        
        self.ids.img6.source = vids[50]['imgUrl']
        self.ids.title6.text = vids[50]['title']
        
        self.ids.img42.source = vids[26]['imgUrl']
        self.ids.title42.text = vids[26]['title']
        
        self.ids.img22.source = vids[15]['imgUrl']
        self.ids.title22.text = vids[15]['title']
        
        self.ids.img32.source = vids[33]['imgUrl']   
        self.ids.title32.text = vids[33]['title']

FilterGrid = GridLayout(cols=5, padding=[10,10,10,10])
parent= FloatLayout()
button= Button()
videos = []
playing_vids = []
class DUIVidPlayerApp(App):

    def build(self):
        self.videos = plistlib.readPlist("Videos.plist") #load videos data
        print self.videos[0]['title'] #title of first video

        self.label = Label(text="Welcome to DiRec.\n", font_size="75sp", pos_hint={'center_x': .5, 'center_y': .5})

        reactor.listenTCP(8000, TCPServerFactory(self))
    	
        parent.add_widget(self.label)
        return parent
     

    def handle_message(self, msg):
        a = msg.split(':')
        command = a[0]
        content = a[1]

        if command == 'detail':
            print "detail"
            print(len(playing_vids))
            if len(playing_vids) is not 0:
                print "we should stop the video!"
                playing_vids[0].state = 'stop'; 
                playing_vids.pop(0) 
            i = int(content)
            detail_widget = DetailWidget(title=self.videos[i]['title'],imageURL=self.videos[i]['imgUrl'], speaker=self.videos[i]['speaker'], duration=self.videos[i]['duration'], descr=self.videos[i]['descr'])
            parent.clear_widgets()
            parent.add_widget(detail_widget)
            return parent

        if command == 'open':
            print "opening home!"
            print(len(playing_vids))
            if len(playing_vids) is not 0:
                print "we should stop the video!"
                playing_vids[0].state = 'stop'; 
                playing_vids.pop(0)     
            home = DUIVidPlayer(self.videos)
            parent.clear_widgets()
            parent.add_widget(home);
            return parent

        if command == 'filter':
            print "filter"
            print(len(playing_vids))
            if len(playing_vids) is not 0:
                print "we should stop the video!"
                playing_vids[0].state = 'stop'; 
                playing_vids.pop(0) 
            i = int(content)
            parent.clear_widgets()
            filter_widget = FilterWidget(title=self.videos[i]['title'],imageURL=self.videos[i]['imgUrl'])
            FilterGrid.add_widget(filter_widget)
            parent.add_widget(FilterGrid)
            return parent

        if command == 'play':
            print(len(playing_vids))
            if len(playing_vids) is not 0:
                print "we should stop the video!"
                playing_vids[0].state = 'stop'; 
                playing_vids.pop(0)   
            i = int(content)
            video= VideoPlayer(source=self.videos[i]['vidUrl'], state='play', pos_hint={'center_y': .5, 'center_y': .5}, allow_fullscreen=1, thumbnail=self.videos[i]['imgUrl'])
            parent.clear_widgets()
            parent.add_widget(video) #add videoplayer
            playing_vids.insert(0,video)
            return parent
    
def reposition_label(root, *args):
	label.x = parent.center_x
	label.y = parent.center_y
        

def on_button_press(self):
    video= VideoPlayer(source='1.mp4', state='play')
    parent.add_widget(video) #add videoplayer
    return parent



if __name__ == '__main__':
    DUIVidPlayerApp().run()