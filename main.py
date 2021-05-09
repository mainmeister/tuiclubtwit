import os

import npyscreen
import clubtwit

class App(npyscreen.NPSAppManaged):

    def onStart(self):
        self.registerForm("MAIN", MainForm())
        self.registerForm("DISPLAY", DisplayShowsForm())
        self.registerForm("PLAY", ShowVideo())

class MainForm(npyscreen.Form):

    def create(self):
        global twitshows
        self.add(npyscreen.TitleText, name="URL:", value=twitshows.url)

    def afterEditing(self):
        self.parentApp.setNextForm("DISPLAY")

class DisplayShowsForm(npyscreen.Form):

    def create(self):
        global twitshows
        showinfo = []
        self.showurls = []
        for show in twitshows.shows():
            showinfo.append(f"{twitshows.pubDate}: {twitshows.title}")
            self.showurls.append(twitshows.url)
        self.titleselector = self.add(npyscreen.TitleSelectOne, name="Shows", values=showinfo)

    def afterEditing(self):
        self.parentApp.setNextForm("PLAY")

    def getItem(self):
        return self.showurls[self.titleselector.value[0]]

class ShowVideo(npyscreen.Form):

    def create(self):
        global twitshows
        self.add(npyscreen.ButtonPress, name='Play', when_pressed_function=self.whenPressed)

    def whenPressed(self):
        global twitshows
        url = app.getForm("DISPLAY").getItem()
        npyscreen.blank_terminal()
        command = eval("f'"+twitshows.streamer+"'")
        npyscreen.notify_confirm(command)
        os.system(command)
        self.editing=False
        #npyscreen.notify_confirm(url,'What to play')

    def afterEditing(self):
        self.parentApp.setNextForm("DISPLAY")

if __name__ == "__main__":
    global twitshows
    twitshows = clubtwit.Shows()
    #for show in twitshows.shows():
        #print(f'{twitshows.pubDate}: {twitshows.title}')
    app = App()
    app.run()