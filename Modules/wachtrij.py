class WachtrijTheorie:
    def __init__(self, aankomst_snelheid, verwerkings_snelheid):
        self._aankomst_snelheid = aankomst_snelheid  # I
        self._verwerkings_snelheid = verwerkings_snelheid  # M
        self._aantal_personen_in_systeem = 0

    def verander_aantal_personen_in_systeem(self, aantal_personen_in_systeem, bereken = False):
        self._aantal_personen_in_systeem = aantal_personen_in_systeem
        
        if bereken:
            self.bereken()

    def verander_aankomst_snelheid(self, aantal, bereken = False):
        self._aankomst_snelheid = aantal

        if bereken:
            self.bereken()

    def bereken(self):
        if self._verwerkings_snelheid == 0:
            raise ValueError("Verwerkings snelheid mag niet 0 zijn.")
        
        self._bezettingsgraad = self._aankomst_snelheid / self._verwerkings_snelheid # G = I / M
        
        if self._aankomst_snelheid == 0:
            self._totale_tijd = 0
            self._service_tijd = 0
            self._wacht_tijd = 0
        else:
            self._totale_tijd = self._aantal_personen_in_systeem / self._aankomst_snelheid # T = N / I
            self._service_tijd = 1 / self._verwerkings_snelheid # S = 1 / M
            self._wacht_tijd = self._totale_tijd - self._service_tijd # W = T - S

    def krijg_bezettings_graad(self):
        return round(self._bezettingsgraad * 100, 2)

    def krijg_totale_tijd(self):
        return round(self._totale_tijd, 2)

    def krijg_service_tijd(self):
        return round(self._service_tijd, 2)
    
    def krijg_actuele_wacht_tijd(self):
        return round(self._aantal_personen_in_systeem * (1 / self._verwerkings_snelheid), 1)

    def krijg_wacht_tijd(self):
        return round(self._wacht_tijd, 2)

    def krijg_aantal_personen_in_systeem(self):
        return round(self._aantal_personen_in_systeem, 2)

    def krijg_aankomst_snelheid(self):
        return round(self._aankomst_snelheid, 2)

    def krijg_verwerkings_snelheid(self):
        return round(self._verwerkings_snelheid, 2)