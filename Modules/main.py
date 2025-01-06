from pyfirmata2 import Arduino, util
from Modules.wachtrij import WachtrijTheorie
import time

class Main:
    # Constante variabelen
    AANKOMST_SNELHEID_INTERVAL: int     = 10
    TIME_DEBOUNCE: float                = 0.05
    KNOP_INDRUK_WAARDE: float           = 0.5
    BOARD: Arduino                      = None
    IT: util                            = None
    BETREDEN_KNOP_PIN: str              = 'a:2:i'
    VERLATEN_KNOP_PIN: str              = 'a:3:i'
    LED_GROEN_PIN: int                  = 9
    LED_GEEL_PIN: int                   = 8
    LED_ROOD_PIN: int                   = 7
    LED_STATUSSEN: list                 = [
                                            0, 
                                            70, 
                                            90
                                        ]
    LED_STOPLICHT: list                 = [
                                            {'led_pin': LED_GROEN_PIN}, 
                                            {'led_pin': LED_GEEL_PIN}, 
                                            {'led_pin': LED_ROOD_PIN}
                                        ]

    # Globale variabelen
    _aankomst_snelheid: int             = 0
    _aantal_personen_in_systeem: int    = 0
    _betreden_knop_waarde: float        = 0
    _verlaten_knop_waarde: float        = 0
    _betreden_knop_status: bool         = False
    _vorige_knop_status: bool           = False
    
    def __init__(self, verwerkings_snelheid: float, capaciteit: int, arduino_port: str):
        # Instellen van de basisvariabelen
        self._verwerkings_snelheid = verwerkings_snelheid
        self._capaciteit = capaciteit
        self._arduino_port = arduino_port 

        # Initialiseren van Arduino en de iterator
        self.BOARD = Arduino(self._arduino_port)
        self.IT = util.Iterator(self.BOARD)
        
        self._wachtrijTheorie: WachtrijTheorie = WachtrijTheorie(0, self._verwerkings_snelheid)
        self._huidige_tijd: float = time.time()
        self._interval_tijd: float = time.time()

        # Configureren van de betreden knop
        self._config_betreden_knop()
        # Configureren van de verlaten knop
        self._config_verlaten_knop()

    # Configuratie voor betreden knop
    def _config_betreden_knop(self) -> None:
        betreden_knop_pin = self.BOARD.get_pin(self.BETREDEN_KNOP_PIN)
        betreden_knop_pin.register_callback(self._callback_betreden_knop)
        betreden_knop_pin.enable_reporting()

    # Configuratie voor verlaten knop
    def _config_verlaten_knop(self) -> None:
        verlaten_knop_pin = self.BOARD.get_pin(self.VERLATEN_KNOP_PIN)
        verlaten_knop_pin.register_callback(self._callback_verlaten_knop)
        verlaten_knop_pin.enable_reporting()

    # Callback voor betreden knop
    def _callback_betreden_knop(self, waarde) -> None:
        self._betreden_knop_waarde = waarde

    # Callback voor verlaten knop
    def _callback_verlaten_knop(self, waarde) -> None:
        self._verlaten_knop_waarde = waarde

    # Tel het aantal personen in het systeem op
    def _tel_aantal_personen_in_systeem_op(self, aantal: int = 1):
        self._aankomst_snelheid += aantal
        self._aantal_personen_in_systeem += aantal
        self._wachtrijTheorie.verander_aantal_personen_in_systeem(self._aantal_personen_in_systeem)
  
        print(f"Aantal personen verhoogd!, Totaal : {self._aantal_personen_in_systeem}")

    # Tel het aantal personen in het systeem af
    def _tel_aantal_personen_in_systeem_af(self, aantal: int = 1):
        self._aantal_personen_in_systeem -= aantal
        self._wachtrijTheorie.verander_aantal_personen_in_systeem(self._aantal_personen_in_systeem)
  
        print(f"Aantal personen verlaagd!, Totaal : {self._aantal_personen_in_systeem}")

    # Controleert of het interval voor aankomst snelheid is verstreken
    def _is_aankomst_snelheid_interval_over(self) -> bool:
        return (self._huidige_tijd - self._interval_tijd) >= self.AANKOMST_SNELHEID_INTERVAL

    # Past de aankomst snelheid aan
    def _pas_aankomst_snelheid_aan(self, aantal: int) -> None:
        self._wachtrijTheorie.verander_aankomst_snelheid(aantal)
        self._wachtrijTheorie.bereken()
        self._aankomst_snelheid = 0

    # Reset het interval voor aankomst snelheid
    def _reset_aankomst_snelheid_interval_check(self) -> None:
        self._interval_tijd = self._huidige_tijd

    # Zet een LED aan
    def _led_aan(self, pin: str) -> None:
        self.BOARD.digital[pin].write(1)

    # Zet een LED uit
    def _led_uit(self, pin: str) -> None:
        self.BOARD.digital[pin].write(0)

    # Zet alle LEDs uit
    def _alle_leds_uit(self) -> None:
        for i in range(len(self.LED_STOPLICHT)):
            self._led_uit(self.LED_STOPLICHT[i]['led_pin'])

    # Schrijf tekst naar het LCD-scherm
    def _schrijf_lcd(self, regel: int, tekst: str):
        # Zorg ervoor dat de tekst altijd 16 karakters lang is, vul met spaties
        tekst = tekst.ljust(16)  # Vul de tekst aan met spaties tot een lengte van 16 karakters
        
        if regel == 1:
            # Voeg '1' toe voor de eerste regel
            data = '1' + tekst  # Voeg de tekst toe voor de eerste regel
            self.BOARD.send_sysex(0x71, util.str_to_two_byte_iter(data))  # Verzend de tekst voor de eerste regel

        elif regel == 2:
            # Voeg '2' toe voor de tweede regel
            data = '2' + tekst  # Voeg de tekst toe voor de tweede regel
            self.BOARD.send_sysex(0x71, util.str_to_two_byte_iter(data))  # Verzend de tekst voor de tweede regel

    # Krijg het aantal resterende personen
    def _krijg_resterende_personen(self):
        if self._capaciteit - self._aantal_personen_in_systeem <= 0:
            return "VOL"
        else:
            return self._capaciteit - self._aantal_personen_in_systeem

    # Bewerk het stoplicht op basis van het aantal personen in het systeem
    def _bewerk_stoplicht(self) -> None:
        rand_voorwaarden = []
        
        # Bereken de drempels voor het aantal personen in het systeem
        for percentage in self.LED_STATUSSEN:
            item = int(self._capaciteit / 100 * percentage)
            rand_voorwaarden.append(item - 1)
        
        # Zet eerst alle LEDs uit
        self._alle_leds_uit()

        # Als er geen mensen in het systeem zijn, zet dan het groene licht aan
        if self._aantal_personen_in_systeem == 0:
            self._led_aan(self.LED_GROEN_PIN)  # Groen licht
            return

        # Voeg het aantal personen in het systeem toe aan de randvoorwaarden
        rand_voorwaarden.append(self._aantal_personen_in_systeem)
        rand_voorwaarden.sort()

        # Bepaal welk licht aan moet op basis van het aantal personen in het systeem
        for i in range(len(rand_voorwaarden)):
            if rand_voorwaarden[i] == self._aantal_personen_in_systeem:
                # Controleer of we de juiste pin voor de LED gebruiken
                led_pin = self.LED_STOPLICHT[i - 1]['led_pin']
                self._led_aan(led_pin)  # Zet het juiste licht aan
                break  # Stop met zoeken zodra het juiste licht aan is

    # Update het LCD-display
    def _update_lcd_display(self):
        self._schrijf_lcd(1, f'Plekken  : {self._krijg_resterende_personen()}')
        self._schrijf_lcd(2, f"Wachttijd: {self._wachtrijTheorie.krijg_actuele_wacht_tijd()}M")

    # Controleer de status van de betreden knop
    def _check_betreden_knop(self, huidige_waarde, vorige_waarde):
        if huidige_waarde >= self.KNOP_INDRUK_WAARDE and vorige_waarde < self.KNOP_INDRUK_WAARDE and self._aantal_personen_in_systeem < self._capaciteit:
            self._tel_aantal_personen_in_systeem_op()

    # Controleer de status van de verlaten knop
    def _check_verlaten_knop(self, huidige_waarde, vorige_waarde):
        if huidige_waarde >= self.KNOP_INDRUK_WAARDE and vorige_waarde < self.KNOP_INDRUK_WAARDE and self._aantal_personen_in_systeem > 0:
            self._tel_aantal_personen_in_systeem_af()

    # Start de hoofd lus
    def start_main_loop(self) -> None:
        self.IT.start()

        vorige_betreden_knop_waarde: float = 0
        vorige_verlaten_knop_waarde: float = 0

        while True:
            self._huidige_tijd = time.time()

            huidige_betreden_knop_waarde = self._betreden_knop_waarde
            huidige_verlaten_knop_waarde = self._verlaten_knop_waarde

            self._check_betreden_knop(huidige_betreden_knop_waarde, vorige_betreden_knop_waarde)
            self._check_verlaten_knop(huidige_verlaten_knop_waarde, vorige_verlaten_knop_waarde)

            vorige_betreden_knop_waarde = huidige_betreden_knop_waarde
            vorige_verlaten_knop_waarde = huidige_verlaten_knop_waarde

            if self._is_aankomst_snelheid_interval_over():
                self._pas_aankomst_snelheid_aan(self._aankomst_snelheid)
                self._reset_aankomst_snelheid_interval_check()
                
            self._bewerk_stoplicht()
            self._update_lcd_display()
            
            time.sleep(self.TIME_DEBOUNCE)

    # Start het programma
    def start(self) -> None:
        print("Program started")

        self._led_aan(self.LED_GROEN_PIN)
        self.start_main_loop()