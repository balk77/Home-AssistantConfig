import appdaemon.plugins.hass.hassapi as hass
from math import ceil


class masterslavezolder(hass.Hass):
    def initialize(self):

        #self.listen_state(self.inputhandler, "sensor.thermostaat_tempsetpoint_raw")
        #self.handle = self.listen_event(self.inputhandler_event, 'MQTT_MESSAGE', namespace = 'mqtt', topic = self.args["roomsp"])
        self.handle = self.listen_event(self.inputhandler_event, 'MQTT_MESSAGE', namespace = 'mqtt', topic = "x/y/z")
        self.listen_state(self.inputhandler_state, self.args["ventipv"])
        self.listen_state(self.inputhandler_state, self.args["thermpv"])
        #self.listen_state(self.inputhandler_state, self.args["roomsp"])

    def inputhandler_state(self, entity, attribute, old, new, kwargs):
        self.main()

    def inputhandler_event(self, event_name, data, kwargs):
        self.main()

    def main(self):

        ventipv = float(self.get_state(self.args["ventipv"]))
        thermpv = float(self.get_state(self.args["thermpv"]))
        roomsp = float(self.get_state(self.args["roomsp"]))

        # self.log(ventipv)
        # self.log(thermpv)
        # self.log(roomsp)
        self.log("room SP is {} degrees".format(roomsp))
        self.log("room PV is {} degrees".format(ventipv))
        self.log("therm PV is {} degrees".format(thermpv))

        if ventipv > roomsp:
            newsp_ = roomsp - (ventipv - thermpv)
            if newsp_ < roomsp:
                #self.log("adjust sp")
                newsp = ceil(2*newsp_)/2
                #self.log(newsp)

        if 'newsp' in locals() and newsp >= 13:
            self.log("Adjust Therm SP, new SP = {}".format(newsp))
            #self.log(newsp)
        else:
            newsp = roomsp
            self.log("Therm SP equal to Room SP")
        
        
        
        self.call_service("mqtt/publish", topic=self.args["thermsp"], payload=newsp)
        #self.fire_event("heaty_set_temp", room_name="zolder", v=str(newsp), reschedule_delay=1)