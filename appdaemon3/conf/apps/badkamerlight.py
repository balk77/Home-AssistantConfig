import appdaemon.plugins.hass.hassapi as hass
import datetime


class badkamerlight(hass.Hass):
    def initialize(self):
        self.override_badkamer_automation = 0
        self.listen_state(self.inputhandler, "light.badkamer_plafond_level", old = "off", new = "on")
        #self.listen_state(self.lightoff, "light.badkamer_plafond_level", old = "on", new = "off")
        dimtime = datetime.time(0, 0, 1)
        brighttime = datetime.time(7, 0, 0)
        self.run_daily(self.changesetting, dimtime,node_id=13,parameter=19,value=10)
        self.run_daily(self.changesetting, brighttime,node_id=13,parameter=19,value=99)
    
    def changesetting(self, kwargs):
        #self.log("setting parameter")
        self.call_service("zwave/set_config_parameter", node_id=kwargs["node_id"],parameter=kwargs["parameter"],value=kwargs["value"])

    def inputhandler(self, entity, attribute, old, new, kwargs):
        if self.override_badkamer_automation == 0:
            now = datetime.datetime.now()
            workday_sensor = self.get_state("binary_sensor.workday_sensor")
            douchecounter = float(self.get_state("counter.douches"))

            # self.setlight(brightness=26, transition=0)
            # self.run_in(self.setlightfade, 20, brightness=255, transition=30)


            if workday_sensor == "on" and now.hour >= 0 and now.hour < 5:
                self.setlight(brightness=26, transition=0)
                self.run_in(self.changesetting, 1,node_id=13,parameter=19,value=10)
            elif workday_sensor == "off" and now.hour >= 0 and now.hour < 7:
                self.setlight(brightness=26, transition=0)
                self.run_in(self.changesetting, 1,node_id=13,parameter=19,value=10)
            # test of Linda en Sander beiden gedoucht hebben
            elif douchecounter < 2:
                if workday_sensor == "on" and now.hour >= 5 and now.hour < 8:
                    self.setlight(brightness=26, transition=0)
                    self.run_in(self.setlightfade, 20, brightness=255, transition=30)
                    self.run_in(self.changesetting, 1,node_id=13,parameter=19,value=10)
                elif workday_sensor == "on" and now.hour >= 8 and self.sun_down() and now.hour < 11:
                    self.setlight(brightness=26, transition=0)
                    self.run_in(self.setlightfade, 20, brightness=255, transition=30)
                    self.run_in(self.changesetting, 1,node_id=13,parameter=19,value=10)
                elif workday_sensor == "off" and now.hour >= 7 and self.sun_down() and now.hour < 11:
                    self.setlight(brightness=26, transition=0)
                    self.run_in(self.setlightfade, 20, brightness=255, transition=30)
                    self.run_in(self.changesetting, 1,node_id=13,parameter=19,value=10)
                else:
                    self.setlight(brightness=254, transition=1)
                    self.run_in(self.changesetting, 1,node_id=13,parameter=19,value=99)
            else:
                self.setlight(brightness=254, transition=1)
                self.run_in(self.changesetting, 1,node_id=13,parameter=19,value=99)

    def setlight(self, brightness, transition):
        self.turn_on("light.badkamer_plafond_level", brightness=brightness, transition=transition)

    def setlightfade(self, kwargs):
        self.turn_on("light.badkamer_plafond_level", brightness=kwargs['brightness'], transition=kwargs['transition'])

    # def lightoff(self, entity, attribute, old, new, kwargs):
    #     self.override_badkamer_automation = 1
    #     self.turn_on("light.badkamer_plafond_level", brightness=1, transition=0)
    #     self.turn_off("light.badkamer_plafond_level")
    #     self.log("badkamer uit") 
    #     self.override_badkamer_automation = 0

