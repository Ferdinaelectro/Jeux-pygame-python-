#Ce jeu a été developpé par Mr ATI TCHAA SOUSSO Ferdinand 

import pygame
import random

pygame.init()

blue = (23,35,255)
white = (255,255,255)
red = (255,45,0)
green = (200,25,255)
#surface principale
pygame.display.set_caption("fenetre de test")
screen = pygame.display.set_mode((800,700))
#class pour l'arme
class arme():
    def __init__(self,surface):
        self.x1 = 0
        self.y1 = 30
        self.x2 = 0
        self.y2 = 80
        self.x3 = 25
        self.y3 = 30
        self.x4 = 50
        self.y4 = 55
        self.r = 12
        self.xc = self.x4 + 25
        self.yc = self.y4 + 12
        #moov attribut : attribut qui permet de deplacer la balle 
        self.moov = False
        #moov_ball attributs : attributs de verification si la balle se deplace 
        self.moov_ball = True
        self.circle_rect_x = (self.xc - self.r)
        self.circle_rect_y = (self.yc - self.r)
        self.screen = surface
        #pas attribut : vitesse de l'arme
        self.pas = 4
        # objet rectangle qui entoure la balle cercle
        self.ball = pygame.Rect(self.circle_rect_x,self.circle_rect_y,24,24)
    #mise à jour des coordonnes du centre du cercle ball
    def update(self):
        self.xc = self.x4 + 25
        self.yc = self.y4 + 12
        self.circle_rect_x = (self.xc - self.r)
        self.circle_rect_y = (self.yc - self.r)
    #creation des objets principaux à mettre dans la surface
    def create(self):
        pygame.draw.circle(screen,red,(self.xc,self.yc),self.r)
        pygame.draw.rect(self.screen,blue,(self.x1,self.y1,25,25))
        pygame.draw.rect(self.screen,blue,(self.x2,self.y2,25,25))
        pygame.draw.rect(self.screen,blue,(self.x3,self.y3,25,75))
        pygame.draw.rect(self.screen,blue,(self.x4,self.y4,25,25))
        # est ce que la balle se deplace : si oui on la créée : grace à create() et en utilisant les coordonnes mise à jour par update()
        if self.moov_ball:
            self.update()
        self.ball = pygame.Rect(self.circle_rect_x,self.circle_rect_y,24,24)
    #fonction pour descendre l'arme fontionnant par incrementation des positions de chaque y
    def descendre(self):
        if (self.y2 + 25)< 700:
            self.y1 += self.pas
            self.y2 += self.pas
            self.y3 += self.pas
            self.y4 += self.pas
            # En incrementant la position des y on utilise update() ,pour mettre à jour les nouvelles positions 
            if self.moov_ball:
                self.update()
    #fonction pour monter l'arme fonctionnant par decrementation des y
    def monter(self):
        if self.y1 >50:
            self.y1 -= self.pas
            self.y2 -= self.pas
            self.y3 -= self.pas
            self.y4 -= self.pas
            # En decrementant la position des y on utilise update() ,pour mettre à jour les nouvelles positions 
            if self.moov_ball:
                self.update()
    # fonction pour tirer la balle 
    def tirer(self):
        # son du coup de feu
        son = pygame.mixer.Sound('coup_de_feu.ogg')
        son.set_volume(0.2)
        son.play()
        # self.moov passe à true pour permettre de deplacer la balle dans la boucle principale 
        self.moov = True
        # quand on tire on rammene self.moov_ball à false pour que les options de descente et de monter de l'arme n'agit pas sur les coordonnes de la balle 
        self.moov_ball = False

# class de l'obstacle
class obstacle():
    # constructeur 
    def __init__(self,screen):
        self.y_obs = 50
        self.x_obs = 700
        self.obstacle = pygame.Rect(self.x_obs,self.y_obs,50,50)
        self.screen = screen
        self.point = 10
        self.end = True
    # fonction pour dessiner l'obstacle sous forme de rectangle
    def creation_obstacle(self):
        self.obstacle = pygame.Rect(self.x_obs,self.y_obs,50,50)
        pygame.draw.rect(self.screen,green,self.obstacle)
    # fonction permettant de generer une position y alléatoire à l'obstacle
    def genere_obstacle(self):
        self.y_obs = random.randint(50,650)
    # fonction pour faire avancer l'obstacle par decremention de x
    def avancer_obs(self):
        # verification si l'obstacle à atteint la fin 
        if self.x_obs > 0:
            #vitesse obstacle
            self.x_obs -= 5
        # si l'obstacle atteint la fin , on genere un autre obstacle de maniere aléatoire grâce au fonction precedente
        else:
            self.x_obs = 700
            self.genere_obstacle()
            self.creation_obstacle()
            self.point -= 1
            print(f"Vous avez perdu {self.point} point")
            # l'obstacle ayant atteint la fin on verifie si les points restants n'atteigne pas 0 ,si oui on remet les points à 10 grace à restart() et on fait passer l'attribut end à false pour faire afficher : game over
            if self.point <= 0:
                self.end = False
                self.restart()
    # remise à niveau des points 
    def restart(self):
        self.point = 10
    # fonction à faire appel si la balle touche l'obstacle
    def obstacle_toucher(self):
        # remise à la position initiale de l'obstacle , pour simuler une disparution
        self.x_obs = 700
        # generation aleatoire et creation d'un nouvelle obstacle, ainsi que sont deplacement
        self.genere_obstacle()
        self.creation_obstacle()
        self.avancer_obs()

# fonction principale du programme
def main():
    # varibles permettant d'ouvrir ou de fermer la fenetre 
    run = True
    # objet time permettant : la limitation à 60 image par seconde
    clk = pygame.time.Clock()
    # creation d'un objet de type : arme
    ar = arme(screen)
    # creation d'un objet de type obstacle 
    obs = obstacle(screen)
    # initialisation de end à true pour pemettre d'ouvrir la fentre de jeu au debut de l'execution du programme
    obs.end = True
    # chargement de la police ubuntu
    police1 = pygame.font.SysFont('ubuntu',30,True)
    # boucle principale infini du jeu 
    while run:
        #boucle de parcours des evènements 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # évènements clavier
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # touche de tabulation pour tirer 
                    ar.tirer()
                if event.key == pygame.K_r:
                    # touche r pour rejouer
                    # fait passer le obs.end à true pour afficher la fenetre de jeu  
                    obs.end = True
                    # appel à la fonction restart pour remettre les points à 10 points
                    obs.restart()
        # chargements  des evenements clavier dans : keys 
        keys = pygame.key.get_pressed()
        # verification si un evenements de maintien de touche fleche bas enfoncées est retrouvées dans les evenements clavier de : keys
        if keys[pygame.K_DOWN]:
            # si evenements de maintien de la touche bas est survenue : execution de la fonction descendre(), pour descendre l'arme
            ar.descendre()
        # verification si l'évènements de maintien enfoncée de la touche fleche haut est trouvées dans les evenements de keys
        if keys[pygame.K_UP]:
            # si evenements trouvées descente de l'arme pas la fonction monter()
            ar.monter()
        if ar.moov:
            # si la moov est à true , alors on peut faire deplacer la balle 
            # verification si la balle n'a pas atteint la fin de l'ecran
            if ar.xc < 800:
                #vitesse de la balle
                ar.xc += 7
                ar.circle_rect_x += 7
            # si la balle a atteint la fin alors on fait:
            else:
                # moov passe à False pour enpecher la balle de se deplacer 
                ar.moov = False
                # moov_ball passe à True pour permettre de mettre à jour les positions de la balle en fonction de la position de l'arme
                ar.moov_ball = True
        # si end est à true alors la fenetre de jeux s'execute dans la boucle infinie 
        if obs.end:
            # verification de la collision de la balle avec l'obstacle 
            if ar.ball.colliderect(obs.obstacle) == True:
                # si oui on execute obstacle_toucher pour remetre à initiale la position de la balle et pour generer un autre obstacle aleatoire 
                obs.obstacle_toucher()
                # moov passe à false pour empecher la balle de se deplacer
                ar.moov = False
                # moov_ball passe à true pour permettre de mettre à jour les positions de la ball en fonction de la position de l'arme
                ar.moov_ball = True
                # ceci c'est pour remettre à jour la balle si ça poosition depace celle de l'obstacle
            """if ar.xc > obs.x_obs + 2:
                ar.moov = False
                ar.moov_ball = True""" 
            # creationdu rectangle qui entoure le cercle               
            pygame.Rect(ar.circle_rect_x,ar.circle_rect_y,24,24)
            # remplissage de la surface par du blanc 
            screen.fill(white)
            # creation de l'arme 
            ar.create()
            # deplacement de la position de l'obstacle 
            obs.avancer_obs()
            # dessinage de l'obstacle
            obs.creation_obstacle()
            # creation de la police et affichage du texte de comptage des points 
            # recuperation du nombre de point grâce à obs.point
            txt1 = police1.render(f"Point : {obs.point}",True,blue)
            screen.blit(txt1,(400,30))
            # bande haut dans la fenetre du jeu pour faire jolie
            pygame.draw.rect(screen,red,(0,0,800,30))
            # mise à jour de l'ecran pour prendre en compte les modifications et limitations du nombre d'images à 60FPS
            pygame.display.flip()
            clk.tick(60)
        # si end est à false execution de la fenetre game over pour arreter le jeu 
        else:
            screen.fill(white)
            # remplissage de l'ecran par du blanc
            # chargements des polices 
            police = pygame.font.SysFont('ubuntu',70,True)
            police1 = pygame.font.SysFont('ubuntu',30,True)
            # rendu ou affichage des textes avec leurs differents polices 
            txt = police.render("GAME OVER !",True,red,blue)
            txt1 = police1.render("Press 'r' for restart",True,blue)
            # superposition du texte par dessus la fenetre principale
            screen.blit(txt,(200,250))
            screen.blit(txt1,(200,350))
            # creation des differents bordures 
            pygame.draw.rect(screen,red,(0,0,800,30))
            pygame.draw.rect(screen,red,(0,0,30,700))
            pygame.draw.rect(screen,red,(770,0,30,700))
            pygame.draw.rect(screen,red,(0,670,800,30))
            # mise à jour de l'ecran pour prendre en compte les modifications grâce à flip()
            pygame.display.flip()
            #limitation à 60 image par seconde 
            clk.tick(60)

# ceci permet d'executer la fonction main lors du lancements du programme
if __name__=='__main__':
    main()