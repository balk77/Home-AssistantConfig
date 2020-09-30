import appdaemon.plugins.hass.hassapi as hass
import datetime

class woonkamer_off(hass.Hass):

  def initialize(self):
    #self.listen_state(self.main2, "input_boolean.test", new="on")
    ## eventjes uit op 3 Feb 2019
    ##self.listen_event(self.main, "zwave.scene_activated", entity_id = "zwave.hank_knop_wk", scene_id = 3)
    self.listen_event(self.main, "zwave.scene_activated", entity_id = "zwave.keuken_koof", scene_id = 24)
    # self.listen_state(self.main2, "input_boolean.lichtknop_wk_links_boven_dubbel", new="on")
    self.listen_state(self.main2, "sensor.lichtknop_wk_links_boven", new="24")
    
    self.counter = 0


  def main2(self, entity, attribute, old, new, kwargs):
    self.main(self,"x","x")

  def main(self, entity, attribute, kwargs):
    now = datetime.datetime.now()
    
    self.log("Alle lampen in woonkamer uit")
    # self.log(self.counter)
    
    # Switch off vacation mode
    self.call_service("input_boolean/turn_off", entity_id="input_boolean.vakantie")

    # activate house sleep mode between 20:00 and 4:00
    if self.now_is_between("20:00:00", "04:00:00"):
    # if now.hour >= 20 or now.hour <= 4:
      self.call_service("input_boolean/turn_on", entity_id="input_boolean.huis_slaapstand")

    # self.log("aan en weer uit")
    # self.call_service("input_boolean/turn_off", entity_id="input_boolean.test")

    delay = self.args["delay"]
    #self.log(entities)
  
    
    self.run_in(self.switch_lights, delay)

  def switch_lights(self, kwargs):
    entityid = self.args["entity_id"]
    entities = self.get_state(entityid, attribute="entity_id")
    for entity in entities:
      # entity_type = entity[:1]
      # if entity_type == "s":
      
      self.call_service("homeassistant/turn_off", entity_id=entity)
      # elif entity_type == "l":
      #   self.call_service("light/turn_off", entity_id=entity)
      
      state = self.get_state(entity)
      #self.log(state)

    self.run_in(self.test_lights, 5)

  def test_lights(self, kwargs):
    entityid = self.args["entity_id"]
    entities = self.get_state(entityid, attribute="entity_id")
    woonkamer_state = "off"
    
    for entity in entities:
      state = self.get_state(entity)
      
      if state == "on":
        # self.log(entity)
        # self.log(state)
        woonkamer_state = "on"
    
    if woonkamer_state == "on" and self.counter < 5:
      self.log("lampen nogmaals schakelen")
      self.main(self,"x","x") 
      self.counter = self.counter + 1
      #self.call_service("homeassistant/turn_off", entity_id=entity_id)
    else:
      self.counter = 0
      


  #  def runout_off(self, entity, attribute, old, new, kwargs):
  #       self.log("runout = uit")
  #       self.run_in(self.switch_runout, 900, action="off")

  #   def switch_runout(self, kwargs):
  #       self.log(kwargs['action'])
  #       if kwargs['action'] == "on":
  #           self.call_service("input_boolean/turn_on", entity_id="input_boolean$
  #       elif kwargs['action'] == "off":
  #           self.call_service("input_boolean/turn_off", entity_id="input_boolea$


