# import appdaemon.plugins.hass.hassapi as hass
# import datetime
# import requests

# # Niet
# # langer
# # in
# # gebruik!!!

# class thermostaat(hass.Hass):
#     def initialize(self):
#         self.listen_state(self.inputhandler, "input_number.hass_tempsetpoint")
#         self.listen_state(self.program_enable, "input_boolean.nefit_programma",new="on")
#         #self.listen_state(self.sync_hass_with_thermostat, "sensor.thermostaat_tempsetpoint")


#     def inputhandler(self, entity, attribute, old, new, kwargs):
#         self.log("ping")
#         temp_sp_hass = float(self.get_state("input_number.hass_tempsetpoint"))
#         temp_sp_thermostaat = float(self.get_state("sensor.thermostaat_tempsetpoint"))

#         headers = {'Content-type': 'application/json'}
#         #myurl = "http://127.0.0.1:8124"
#         myurl = "http://192.168.0.9:8124"
#         command1 = "/bridge/heatingCircuits/hc1/temperatureRoomManual"
#         command2 = "/bridge/heatingCircuits/hc1/manualTempOverride/status"
#         command3 = "/bridge/heatingCircuits/hc1/manualTempOverride/temperature"

#         body1 = temp_sp_hass
#         body2 = "on"
#         body3 = temp_sp_hass
#         self.log("new setpoint & command:")
#         self.log(body1)
#         self.log(body2)

#         if(temp_sp_hass != temp_sp_thermostaat):

#             r1 = requests.post(myurl+command1, verify=False, json={"value": body1}, headers = headers)
#             self.log(r1.status_code)
#             self.log(r1.text)

#             r2 = requests.post(myurl+command2, verify=False, json={"value": body2}, headers = headers)
#             self.log(r2.status_code)
#             self.log(r2.text)

#             r3 = requests.post(myurl+command3, verify=False, json={"value": body3}, headers = headers)
#             self.log(r3.status_code)
#             self.log(r3.text)

#             self.call_service("input_boolean/turn_off", entity_id="input_boolean.nefit_programma")

#             #self.set_state("input_boolean.nefit_programma", state="off")




#     def program_enable(self, entity, attribute, old, new, kwargs):

#         headers = {'Content-type': 'application/json'}
#         #myurl = "http://127.0.0.1:8124"
#         myurl = "http://192.168.0.9:8124"
#         command2 = "/bridge/heatingCircuits/hc1/manualTempOverride/status"

#         body2 = "off"


#         r2 = requests.post(myurl+command2, verify=False, json={"value": body2}, headers = headers)
#         self.log(r2.status_code)
#         self.log(r2.text)

#     # def sync_hass_with_thermostat(self, entity, attribute, old, new, kwargs):
        
#     #     temp_sp_thermostaat = float(self.get_state("sensor.thermostaat_tempsetpoint"))

#     #     self.log(temp_sp_thermostaat)

#     #     self.call_service("input_number/set_value", entity_id="input_number.hass_tempsetpoint", value=temp_sp_thermostaat)

#     #     #self.set_value("input_number.hass_tempsetpoint", temp_sp_thermostaat)
