from basisklassen import *
import click
import time
import json

class BaseCar(object):
    """
    Basisklasse fuer Antrieb und Lenkung des Picar
    FrontWheel und BackWheels werden als Objekte instanziert
        
    """
    def __init__(self) -> None:

        try:
            with open("config.json", "r") as f:
                data = json.load(f)
                turning_offset = data["turning_offset"]
                forward_A = data["forward_A"]
                forward_B = data["forward_B"]
                print("Daten in config.json:")
                print(" - Turning Offset: ", turning_offset)
                print(" - Forward A: ", forward_A)
                print(" - Forward B: ", forward_B)
        except:
            print("Keine geeignete Datei config.json gefunden!")
        self.fw = FrontWheels(turning_offset=turning_offset) # turning_offset übergeben zur Justierung des Lenkeinschlags
        self.bw = BackWheels()
        self.steering_angle = 90
        self.speed = 0 
        self._direction = 0

    
    @property
    def steering_angle(self)-> int :
        """Getter für die Lenkwinkel-Abfrage, gibt Winkel als int zurück"""
        return self._steering_angle
    
    @steering_angle.setter
    def steering_angle(self, angle: int)-> None:
        """Setter für Lenkwinkel
        Args:
        angle(int): Lenkwinkel, welcher eingestellt werden soll
        Eingabewert zwischen 45 und 135
        """
        self._steering_angle = angle
        self.fw.turn(angle)
    
    @property
    def direction(self)-> int:
        """Getter für Einstellung der Fahrtrichtung
            -1 : Rückwärts
            0  : STOP
            1  : Vorwärts
        """
        return self._direction

    @property
    def speed(self)-> int:
        """Getter für Geschwindigkeit
        Einstellung zwischen 0 und 100"""
        return self._speed

    @speed.setter
    def speed(self, speed: int)-> None:
        """Setter für Geschwindigkeit
        Args:
        speed(int): Setzen der Umdrehungsgeschwindigkeit der Räder
        """
        self._speed = speed
        self.bw.speed = speed
    
    def drive(self, speed:int, direction:int):
        """Methode zum Fahren
        
        Args: 
        Geschwindigkeit und Fahrtrichtung
        speed(int): Setzen der Umdrehungsgeschwindigkeit der Räder (0 und 100)
        direction(int): Einstellung der Fahrtrichtung
            -1 : Rückwärts
            0  : STOP
            1  : Vorwärts
        """
       
        self.speed = speed

        if direction == 1:
            print("Fahre vorwärts")
            self._direction = 1
            self.bw.forward()
        elif direction == -1:
            print("Fahre rückwärts")
            self._direction = -1
            self.bw.backward()
            
        elif direction == 0:
            print("Stop")
            self._direction = 0
            self.bw.stop()
        else:
            print("Ungültige Fahrtrichtungsangabe")
    
    def stop(self):
        """Methode zum Stoppen
        
        """
        self.bw.stop()


#### Main ####

@click.command()
@click.option('--modus', '--m', type=int, default=None, help="Startet Test für Klasse direkt.")
def main(modus):
    """Function for choosing the parcours


    Args:
        modus (int): The mode that can be choosen by the user
    """
    print('-- Auswahl der Fahrfunktionen --------------------')
    modi = {
        0: 'Ausrichtung der Servo der Lenkung auf Geradeaus',
        1: 'Fahrparcours 1 - Vorwärts und Rückwärts',
        2: 'Fahrparcours 2 - Kreisfahrt mit maximalem Lenkwinkel',
        # 3: 'Test Ultraschallmodul / Klasse: Ultrasonic',
        # 4: 'Test Infrarotmodul / Klasse: Infrared',
        # 5: 'Test Hinter- und Vorderräder unter Verwendung der Konfigurationen in config.json',
    }

    if modus == None:
        print('--' * 20)
        print('Auswahl:')
        for m in modi.keys():
            print('{i} - {name}'.format(i=m, name=modi[m]))
        print('--' * 20)

    while modus == None:
        try:
            modus_list = list(modi.keys())
            modus = int(input('Wähle  (Andere Taste für Abbruch): ? '))
            modus = modus_list[modus]
            break
        except:
            print('Getroffene Auswahl nicht möglich.')
            quit()

    if modus == 0:
        print('Der Servomotor wird nach rechts und links bewegt und dann auf geradeus ausgerichtet.')
        bc = BaseCar()
        bc.steering_angle = 45
        time.sleep(.5)
        bc.steering_angle = 135
        time.sleep(.5)
        bc.steering_angle = 90
        x=input('Servo der Lenkung auf 90 Grad/geradeaus ausgerichtet! (ENTER zum beenden)')

    if modus == 1:
        x = input('ACHTUNG! Das Auto wird ein Stück vor und zurück fahren!\n Drücken Sie ENTER zum Start.')
        if x == '':
            print('Fahrparcours 1')
            bc = BaseCar()
            bc.drive(30, 1)
            time.sleep(3)
            bc.drive(0, 0)
            time.sleep(1)
            bc.drive(30, -1)
            time.sleep(3)
            bc.drive(0, 0)
            print("Ende des Parcours.")
        else:
            print('Abbruch.')

    if modus == 2:
        
        x = input(' ACHTUNG! Das Auto wird nach kurzer Geradeausfahrt verschiedene Kreise fahren!\n Drücken Sie ENTER zum Start.')
        if x == '':
            print('Fahrparcours 2')
            bc = BaseCar()
            bc.steering_angle = 90
            bc.drive(30, 1)
            time.sleep(1)
            bc.steering_angle = 135
            time.sleep(8)
            bc.drive(0, 0)
            bc.drive(30, -1)
            time.sleep(8)
            bc.steering_angle = 90
            time.sleep(1)
            bc.drive(0, 0)
            time.sleep(.5)
            bc.drive(30, 1)
            time.sleep(1)
            bc.steering_angle = 45
            time.sleep(8)
            bc.drive(0, 0)
            bc.drive(30, -1)
            time.sleep(8)
            bc.steering_angle = 90
            time.sleep(1)
            bc.drive(0, 0)
            print("Ende des Parcours.")
        else:
            print('Abbruch.')
        


if __name__ == '__main__':
    main()