
#CO2ppm = data.get('CO2ppm')
trigger_type = data.get('trigger_type')
fanstatustime = float(data.get('fanstatustime'))


minhum = float(hass.states.get('sensor.minhum').state)
badkamer_abshumidity = float(hass.states.get('sensor.badkamer_abshumidity').state)

# history uit influxdb om laagste waarde in afgelopen x tijd te bepalen
#https://home-assistant.io/components/sensor.influxdb/

boilerstatus = hass.states.get('sensor.wk_boilerstatus').state
oldfanspeed = hass.states.get('sensor.itho_ventilatie').state


logger.error("Minimum humidity {}".format(minhum))




#logger.error("boilerstatuslastchange {}".format(boilerlastupdated))



threshold = 15

if(trigger_type == "HW" and boilerstatus == "HW"):
    fanspeed = "high"
elif(trigger_type == "humidity"):
    if(fanstatustime < 1200 and oldfanspeed == "high"):
        fanspeed = "high"
    elif (badkamer_abshumidity >= minhum + 4):
        fanspeed = "high"
    elif(badkamer_abshumidity > minhum + 2 and badkamer_abshumidity < minhum + 4):
        fanspeed = "medium"
    else:
        fanspeed = "low"

hass.services.call("mqtt","publish",{ "topic" : "/hass/itho", "payload" : fanspeed })
