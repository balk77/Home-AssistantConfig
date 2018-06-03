import appdaemon.plugins.hass.hassapi as hass


class zonnescherm(hass.Hass):
    def initialize(self):
        # Listen for state change of ventilation requirements
        self.listen_state(self.input_parse, "sensor.azimuth")
        self.run_at_sunset(self.open_cover)
        #self.listen_state(self.input_parse, "sensor.badkamer_abshumidity")

        # DesiredPercentage = self.get_state("input_number.zolder_ventilatie")

    def input_parse(self, entity, attribute, old, new, kwargs):
        azimuth = float(self.get_state("sensor.azimuth"))
        irradiance = float(self.get_state("sensor.delft_irradiance"))
        precipitation = float(self.get_state("sensor.delft_precipitation_forecast_total"))

        if 54 < azimuth < 234:
            sun_at_back = True
        else:
            sun_at_back = False

        #self.log(irradiance)

        if precipitation > 0.1:
            self.open_cover()
        elif irradiance > 600 and sun_at_back:
            self.close_cover()
        elif not sun_at_back:
            self.open_cover()
        else:
            self.open_cover()

    def close_cover(self):

        curstate = self.get_state("cover.level", attribute="current_position")
        #self.log(curstate)

        if curstate != 20:
            self.call_service("cover/set_cover_position", entity_id="cover.level", position="20")



    def open_cover(self):
        curstate = self.get_state("cover.level", attribute="current_position")

        #curstate = self.get_state("cover.level")
        #self.log(curstate)

        if curstate != 100:
            self.call_service("cover/set_cover_position", entity_id="cover.level", position="100")

        # if curstate != "open":
        #     self.call_service("cover/open_cover", entity_id="cover.level")
