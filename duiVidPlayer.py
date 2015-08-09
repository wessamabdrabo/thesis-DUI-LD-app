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

class DUIVidPlayer(FloatLayout):    
    def __init__(self, **kwargs):
        super(DUIVidPlayer, self).__init__(**kwargs)
        print "in DUIVidPlayer"
        vids = ['https://tedcdnpi-a.akamaihd.net/r/tedcdnpe-a.akamaihd.net/images/ted/7ee0e10094b7da17d2d14e91b9cf481fa512a782_2880x1620.jpg?ll=1&amp;quality=89&amp;w=800',
            'https://tedcdnpi-a.akamaihd.net/r/tedcdnpe-a.akamaihd.net/images/ted/fbada01990f86f5afa850cc23a0259fec091f929_2880x1620.jpg?ll=1&amp;quality=89&amp;w=800',
            'https://tedcdnpi-a.akamaihd.net/r/tedcdnpe-a.akamaihd.net/images/ted/f9f08b68e8971ade2d347b3000b6cd2bd448626c_2880x1620.jpg?ll=1&amp;quality=89&amp;w=800',
            'https://tedcdnpi-a.akamaihd.net/r/tedcdnpe-a.akamaihd.net/images/ted/2b3dff7f7dffeb2228830bacdf591ac5cfdddc9b_2880x1620.jpg?ll=1&amp;quality=89&amp;w=800',
            'https://tedcdnpi-a.akamaihd.net/r/tedcdnpe-a.akamaihd.net/images/ted/2f500bfac6fa50bc2abe67459d36c9c3f0e3e48a_2880x1620.jpg?ll=1&amp;quality=89&amp;w=800',
            'https://tedcdnpi-a.akamaihd.net/r/tedcdnpe-a.akamaihd.net/images/ted/0438f3c9c66aff53ca7b549459d6e081dd7bea6f_2880x1620.jpg?ll=1&amp;quality=89&amp;w=800']
        self.ids.img1.source = vids[1]
        self.ids.img2.source = vids[3]
        self.ids.img3.source = vids[4]
        self.ids.img4.source = vids[2]
        self.ids.img5.source = vids[5]
        self.ids.img6.source = vids[5]
        self.ids.img42.source = vids[3]
        self.ids.img22.source = vids[2]
        self.ids.img32.source = vids[1]


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
        if msg == 'open':
            print "opening home!"
            home = DUIVidPlayer()
            parent.add_widget(home);
            return parent
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