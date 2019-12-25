import appdaemon.plugins.hass.hassapi as hass
#
# Hellow World App
#
# Args:
#

class HelloWorld(hass.Hass):

  def initialize(self):
    self.log("Hello from AppDaemon")
    #  self.log("You are now ready to run Apps!m")
    #  self.log("")
    #  self.log("")
    #  self.log(self.sun_up()) 

    #  self.notify("lalalalla")
    # self.handle = self.listen_event(self.inputhandler, "call_service", domain = "climate", service = "set_temperature")
    # , "climate.set_temperature")
    # , entity_id = "climate.woonkamer")

  # def inputhandler(self, event_name, data, kwargs):
    
    
  #   self.log(data)
  #   # self.log(data['service_data']['entity_id'])
  #   entity_id = data['service_data']['entity_id']
  #   temperature = data['service_data']['temperature']
  #   self.log(entity_id)
  #   self.log(temperature)
    


