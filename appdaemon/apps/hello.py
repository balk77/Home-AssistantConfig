import appdaemon.appapi as appapi

#
# Hello World App
#
# Args:
#

class HelloWorld(appapi.AppDaemon):

  def initialize(self):
     self.log("Hello from AppDaemon222222")
     self.log("You are now ready to run Apps223!")
