import appdaemon.appapi as appapi
import datetime

#
# Hello World App
#
# Args:
#

class HelloWorld(appapi.AppDaemon):

  def initialize(self):
     self.log("Hello from AppDaemon222222")
     self.log("You are now ready to run Apps223!")
     # self.log(datetime.datetime.now())
     # self.log(self.sunrise())
     # if datetime.datetime.now() > self.sunrise():
     #     self.log("na zonsopgang")
     # else:
     #    self.log("voor zonsopgang")
