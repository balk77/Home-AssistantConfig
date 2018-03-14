import appdaemon.appapi as appapi
import math

class rel2abs(appapi.AppDaemon):
    def initialize(self):
        self.listen_state(self.inputhandler, self.args["relhumidity"])

    def inputhandler(self, entity, attribute, old, new, kwargs):
        temperature = float(self.get_state(self.args["temperature"]))
        relhumidity = float(self.get_state(self.args["relhumidity"]))


        abshumidity = round((6.112 * math.exp((17.67 * temperature)/(temperature+243.5)) * relhumidity * 2.1674)/(273.15+temperature),2);
        self.log("abshumidity")
        self.log(abshumidity)

        status = self.set_state(self.args["abshumidity"], state=abshumidity, attributes={"unit_of_measurement":"mg/m3"})
        self.call_service("mqtt/publish", topic=self.args["topic"], payload=abshumidity)
