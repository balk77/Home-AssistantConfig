import appdaemon.plugins.hass.hassapi as hass
#
# Hellow World App
#
# Args:
#

class mqtttest(hass.Hass):

  def initialize(self):
    self.log("Hello from MQTT Test")
    self.log("")
    self.log("")

    #config = self.get_plugin_config()
    #self.log(config)
    #self.log("Current Client ID is {}".format(config["client_id"]))
    #self.call_service(self, 
    self.handle = self.listen_event(self.mqtt_callback, 'MQTT_MESSAGE', namespace = 'mqtt')

    

  def mqtt_callback(self, event_name, data, kwargs):
    
    # do something with the received payload
    self.log(data['payload'])