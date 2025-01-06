from pyfirmata2 import Arduino, util

class LCD:
    def __init__(self, board: Arduino):
        self.board = board

    # Schrijf tekst naar het LCD-scherm
    def schrijf(self, regel: int, tekst: str):
        # Zorg ervoor dat de tekst altijd 16 karakters lang is, vul met spaties
        tekst = tekst.ljust(16)  # Vul de tekst aan met spaties tot een lengte van 16 karakters
        
        if regel == 1:
            # Voeg '1' toe voor de eerste regel
            data = '1' + tekst  # Voeg de tekst toe voor de eerste regel
            self.board.send_sysex(0x71, util.str_to_two_byte_iter(data))  # Verzend de tekst voor de eerste regel

        elif regel == 2:
            # Voeg '2' toe voor de tweede regel
            data = '2' + tekst  # Voeg de tekst toe voor de tweede regel
            self.board.send_sysex(0x71, util.str_to_two_byte_iter(data))  # Verzend de tekst voor de tweede regel
