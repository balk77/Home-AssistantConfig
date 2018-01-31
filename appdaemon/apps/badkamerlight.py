import appdaemon.appapi as appapi
import datetime


class badkamerlight(appapi.AppDaemon):
    def initialize(self):
        self.listen_state(self.inputhandler, "light.badkamer_plafond_level", old = "off", new = "on")

    def inputhandler(self, entity, attribute, old, new, kwargs):
        now = datetime.datetime.now()
        workday_sensor = self.get_state("binary_sensor.workday_sensor")

        # self.setlight(brightness=26, transition=0)
        # self.run_in(self.setlightfade, 20, brightness=255, transition=30)


        if workday_sensor == "on" and now.hour >= 0 and self.sun_down() and now.hour < 5:
            self.setlight(brightness=26, transition=0)
        elif workday_sensor == "off" and now.hour >= 0 and self.sun_down() and now.hour < 7:
            self.setlight(brightness=26, transition=0)
        elif workday_sensor == "on" and now.hour >= 5 and self.sun_down() and now.hour < 11:
            self.setlight(brightness=26, transition=0)
            self.run_in(self.setlightfade, 20, brightness=255, transition=30)
        elif workday_sensor == "off" and now.hour >= 7 and self.sun_down() and now.hour < 11:
            self.setlight(brightness=26, transition=0)
            self.run_in(self.setlightfade, 20, brightness=255, transition=30)
        else:
            self.setlight(brightness=254, transition=0)

    def setlight(self, brightness, transition):
        self.turn_on("light.badkamer_plafond_level", brightness=brightness, transition=transition)

    def setlightfade(self, kwargs):
        self.turn_on("light.badkamer_plafond_level", brightness=kwargs['brightness'], transition=kwargs['transition'])
