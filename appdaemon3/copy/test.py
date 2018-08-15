import appdaemon.plugins.hass.hassapi as hass

class test(hass.Hass):

    def initialize(self):
        self.listen_state(self.what_we_want_to_do,"input_boolean.occupancy_simulation", new="on")
        self.log("Hello from AppDaemon")

    def what_we_want_to_do(self, entity, attribute, old, new, kwargs):
        a_variabele_with_a_usable_name = self.get_state("device_tracker.phone_nexus5x")
        self.log("Hello from AppDaemon")

        if  a_variabele_with_a_usable_name == "home":
            self.turn_off("switch.fibaro_switch_switch")
            self.turn_on("switch.fibaro_switch_switch")
