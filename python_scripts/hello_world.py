name = data.get('name', 'world')
logger.info("Hello {}".format(name))
hass.bus.fire("notify",{ "message" : "testtt" })
#hass.bus.ServiceCall("notify","notify",{ "message" : "testtt" })
#hass.bus.call_service("notify","notify",{ "message" : "testtt" })
hass.bus.fire(name, { "wow": "from a Python script!" })
