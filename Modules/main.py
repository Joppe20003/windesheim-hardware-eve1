from Modules.wachtrij import WachtrijTheorie

class Main:
    def __init__(self):
        self._verwerkings_snelheid = 10
        self._aantal_personen_in_systeem = 0
        self._wachtrijTheorie = WachtrijTheorie(self._verwerkings_snelheid, self._aantal_personen_in_systeem)

    def start(self):
        pass