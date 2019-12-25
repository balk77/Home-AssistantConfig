import appdaemon.plugins.hass.hassapi as hass
import datetime


class itho(hass.Hass):
    def initialize(self):
        self.log("Hello from AppDaemon")

        
        # self.handle = self.listen_state(self.front_to_esp, "input_boolean.fansendtimer1_front", new="on")
        # self.handle = self.listen_state(self.front_to_esp, "input_boolean.fansendtimer2_front", new="on")
        # self.handle = self.listen_state(self.front_to_esp, "input_boolean.fansendtimer3_front", new="on")
        # self.handle = self.listen_state(self.front_to_esp, "input_boolean.fansendlow_front", new="on")
        # self.handle = self.listen_state(self.front_to_esp, "input_boolean.fansendhigh_front", new="on")
        # self.handle = self.listen_state(self.front_to_esp, "input_boolean.fansendmedium_front", new="on")
        # self.handle = self.listen_state(self.front_to_esp, entity_id="fan.itho_front", new="on")
        # self.listen_event(self.front_to_esp, "zwave.scene_activated", scene_id = 3)
        # , attribute="fansendtimer1_front")
        # , new="on")

    
    def front_to_esp(self, entity, attribute, old, new, kwargs):
        self.log("Hello from AppDaemon")
        self.log(self.get_state("fan.itho_front"))
        # entityid = self.info_listen_state(self.handle)[1]
        # entity_short = entityid[-1*(len(entityid)-len("input_boolean.")):]
        # entity_short_esp = entity_short[:len(entity_short)-len("_front")]

        # self.log(entity_short_esp)

        # if entity_short_esp == "fansendlow":
        #     esp_speed = 'Low'
        # elif entity_short_esp == "fansendmedium":
        #     esp_speed = 'Medium'
        # elif entity_short_esp == "fansendmhigh":
        #     esp_speed = 'High'
        # elif entity_short_esp == "fansendtimer1":
        #     esp_speed = 'Timer 1'
        # elif entity_short_esp == "fansendtimer2":
        #     esp_speed = 'Timer 2'
        # elif entity_short_esp == "fansendtimer3":
        #     esp_speed = 'Timer 3'
        # else:
        #     esp_speed = 'Low'
        

        # self.call_service("fan/turn_on", entity_id="fan.itho_esphome", speed=esp_speed)
        # self.call_service("input_boolean/turn_off", entity_id="input_boolean."+entity_short)

        # self.log(esp_speed)




        
