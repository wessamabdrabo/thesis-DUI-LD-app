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

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.videoplayer import VideoPlayer

parent= FloatLayout()
button= Button()

class DUIVidPlayerApp(App):

    def build(self):
        pl = plistlib.readPlist("Videos.plist") #load videos data
        print pl[0]['title'] #title of first video

        self.label = Label(text="server started\n", pos_hint={'center_x': .5, 'center_y': .5})

    	reactor.listenTCP(8000, TCPServerFactory(self))
    	
        parent.add_widget(self.label)
        return parent

    def handle_message(self, msg):
        print "video url: " + msg
        video= VideoPlayer(source=msg, state='play', pos_hint={'center_y': .5, 'center_y': .5})
        parent.add_widget(video) #add videoplayer
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