import appdaemon.plugins.hass.hassapi as hass
import datetime

class test(hass.Hass):

  def initialize(self):
    self.log("test")
    #self.listen_state(self.main2, "input_boolean.test", new="on")
    ## eventjes uit op 3 Feb 2019
    ##self.listen_event(self.main, "zwave.scene_activated", entity_id = "zwave.hank_knop_wk", scene_id = 3)
    # self.listen_event(self.main, "zwave_js_value_notification", node_id = 12, value = 24)
    # self.listen_state(self.main2, "input_boolean.lichtknop_wk_links_boven_dubbel", new="on")
    # self.listen_state(self.main2, "sensor.lichtknop_wk_links_boven", new="24")
            # self.call_service("zwave_js/set_config_parameter", entity_id="light.badkamer_plafond_level", parameter="Forced switch on brightness level", value=99)



  # def main(self, entity, attribute, kwargs):
    # self.call_service("light/toggle", entity_id="light.wk_muur_level")
