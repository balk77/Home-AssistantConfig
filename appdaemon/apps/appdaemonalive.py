import appdaemon.appapi as appapi
import time
import datetime


class appdaemonalive(appapi.AppDaemon):
    def initialize(self):
        time = datetime.time(0, 0, 0)

        self.run_minutely(self.set_alive, time)


    def set_alive(self, kwargs):
        self.log("AppDaemon = alive")


        self.set_state("input_boolean.appdaemon_alive", state="on")
