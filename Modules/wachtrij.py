class WachtrijTheorie:
    def __init__(self, verwerkings_snelheid: float, aantal_personen_in_systeem: float):
        self._verwerkings_snelheid = verwerkings_snelheid  # μ: Verwerkingssnelheid
        self._aantal_personen_in_systeem = aantal_personen_in_systeem  # N: Personen in systeem

        # Aannames en berekeningen
        self._aankomst_snelheid = self._aantal_personen_in_systeem * self._verwerkings_snelheid / (self._aantal_personen_in_systeem + 1)  # λ (geschat)
        self._bezettings_graad = self._aankomst_snelheid / self._verwerkings_snelheid * 100  # g = λ / μ * 100

        # Wachttijdberekeningen volgens wachtrijtheorie
        self._totale_tijd = 1 / (self._verwerkings_snelheid - self._aankomst_snelheid)  # T = 1 / (μ - λ)
        self._service_tijd = 1 / self._verwerkings_snelheid  # S = 1 / μ
        self._wacht_tijd = self._totale_tijd - self._service_tijd  # W = T - S

    def bezettings_graad(self, decimalen: float) -> float:
        return self.afr(self._bezettings_graad, decimalen)

    def totale_tijd(self) -> float:
        return self._totale_tijd

    def service_tijd(self) -> float:
        return self._service_tijd

    def wacht_tijd(self) -> float:
        return self._wacht_tijd

    def aankomst_snelheid(self) -> float:
        return self._aankomst_snelheid
    
    def afr(self, getal: float, decimalen: float) -> float:
        return round(getal, decimalen)