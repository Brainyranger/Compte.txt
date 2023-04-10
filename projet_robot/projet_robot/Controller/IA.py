import time
import math
from threading import Thread
from projet_robot.Simulation.Robot import Robot
from projet_robot.Controller.Proxy import largeur_robot,Proxy_simulation as proxy_simul,Proxy_reel


class IA(Thread):

    def __init__(self,ia_command):
        """ constructeur de notre classe IA
            initialisation de notre liste de commandes
            initialisation de l'état de notre commande courante"""


        super(IA,self).__init__()
        self.status = True
        self.ia_command = ia_command
        self.curr_command = 0

    def update(self,dt):
        """ Parcoure notre liste de commandes et éxécute commande par commande """

        if len(self.ia_command) == 0:
            self.status = False
            return
            
        if self.stop():
            self.status = False
            return

        if self.curr_command < len(self.ia_command) and self.ia_command[self.curr_command].stop():
            self.curr_command += 1
            self.ia_command[self.curr_command].start()
        
        self.ia_command[self.curr_command].update(dt)       

    def ajout_commandes(self,command):
        """ Ajout d'une commande à la liste de commandes """

        self.ia_command.append(command)
        
    def stop(self):
        """ Arret de l'IA """
        return self.curr_command == len(self.ia_command)-1 and self.ia_command[self.curr_command].stop()
        
        
    def getStatus(self):
        """ Renvoie l'état de l'IA """

        return self.status

    def	select_commandes(self,indice):
        """ selectionne par indice notre commande """
        if indice < 0 or indice > len(self.ia_command):
            return 
        return self.ia_command[indice]



class Avancer:

    def __init__(self,vitesse,distance,robot):
        """ constructeur de notre classe Avancer
        initialisation de la vitesse de nos roues 
        initialisation de la distance à parcourir
        initialisation de notre robot pour lequel on applique la comande"""

        self.robot = Proxy_reel(robot,vitesse,0)
        self.distance = distance
        self.status = False
    
    def update(self,dt) :
        """ Fais la mise à jour de notre déplacement en ligne droite """
	
        

        if self.stop():
            self.robot.reset()
            self.status = False
            return
        self.robot.avancer()
        self.robot.update_distance_parcourue(dt)
        print("Le robot a parcouru " + str(self.robot.distance_parcourue))
         	
        	
    def getStatus(self):
        """ Renvoie l'état de la commande """

        return self.status

    def start(self):
        """ Lance la commande """
        self.robot.reinitialiser_distance_parcourue()
        self.status = True

    def stop(self):
        """ Arret de la commande en cours"""
        return self.robot.get_distance_parcourue() >= self.distance 


class Tourner:

    def __init__(self,vitesse,angle,robot):
        """ Constructeur de notre classe Tourner 
        initialisation de la vitesse de nos roues
        initialisation de l'angle qu'on doit parcourir 
        initialisation de la distance à parcourir en degré/s pour parcourir l'angle
        initialisation de notre robot pour lequel on applique la comande"""

        self.robot = Proxy_reel(robot,vitesse,angle)
        self.angle = angle
        self.angle_parcouru = 0
        self.status = True

        
    def update(self,dt):
        """ Fais la mise à jour de notre commande """

        if self.stop():
            self.robot.reset()
            self.status = False
            return
        
        self.robot.update_angle_parcouru(dt)
        self.robot.tourner()
        print("j'ai fini de parcourir "+str(self.robot.angle_parcouru)+" degré")
       
	
    def getStatus(self):
        """ Renvoie l'état de la commande """

        return self.status

    def start(self):
        """ Lance la commande """
        self.robot.reinitialiser_angle_parcouru()
        self.status = True

    def stop(self):
        """ Arrête la commande en cours """

        return self.robot.get_angle_parcouru() > abs(self.angle)
    

