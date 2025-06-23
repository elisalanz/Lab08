import flet as ft

from model.nerc import Nerc


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._idMap = {}
        self.fillIDMap()

    def handleWorstCase(self, e):
        if self._view._ddNerc.value is None or self._view._txtYears.value is None or self._view._txtHours.value is None:
            self._view.create_alert("Complete all fields!")
        nerc_value = self._view._ddNerc.value
        try:
            years = int(self._view._txtYears.value)
            hours = float(self._view._txtHours.value)
        except ValueError:
            self._view.create_alert("Please enter a number.")
        events, tot_hours, tot_people_affected = self._model.worstCase(nerc_value, years, hours)
        txt_out = f"Tot people affected: {tot_people_affected}\nTot hours of outage: {tot_hours}\n"
        for event in events:
            txt_out += str(event) + "\n"
        self._view._txtOut.controls.append(ft.Text(txt_out))
        self._view._ddNerc.value = None
        self._view._txtYears.value = None
        self._view._txtHours.value = None
        self._view.update_page()
        self._view._txtOut.controls.clear()

    def fillDD(self):
        nercList = self._model.listNerc

        for n in nercList:
            self._view._ddNerc.options.append(ft.dropdown.Option(n))
        self._view.update_page()

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v
