import appdaemon.plugins.hass.hassapi as hass

class sensorexport(hass.Hass):
    def initialize(self):
        self.listen_state(self.inputhandler, self.args["trigger"])

    def inputhandler(self, entity, attribute, old, new, kwargs):
        payload = self.get_state(self.args["trigger"])

        topic = "/"+self.args["location"]+"/"+self.args["sublocation"]+"/"+self.args["sensor"]+"/"+self.args["property"]

        self.call_service("mqtt/publish", topic=topic, payload=payload)
