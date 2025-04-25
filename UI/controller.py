import flet as ft

from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        self._view.lst_result.controls.clear()
        res=self._model.get_Umidita_Media(self._mese)

        if self._mese==0:
            self._view.create_alert("Selezionare un mese!")
            return

        if res==[]:
            self._view.lst_result.controls.append(ft.Text("Non ci sono dati disponibili per il mese indicato"))
            self._view.update_page()
        else:
            self._view.lst_result.controls.append(ft.Text("L'umidità media nel mese selezionato è: "))
            for r in res:
                self._view.lst_result.controls.append(ft.Text(r))
            self._view.update_page()


    def handle_sequenza(self, e):
        pass

    def read_mese(self, e):
        self._mese = int(e.control.value)

