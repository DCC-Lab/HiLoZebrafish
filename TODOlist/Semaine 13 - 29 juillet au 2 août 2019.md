Maxence :
  - Regrouper les informations sur l'optique et rédiger un document informatif. 
  - Expérience sur l'angle du diffuseur DG10-600 avec le puissance mètre afin de situer le niveau de grit du LSR-3005. *Hypothèse : Niveau de grit entre le DG10-600 et le DG10-1500.*
  - Prendre des z-stacks avec le sutter motion controller de Charles. 
      
Valérie :
  - Commence dont ton affiche pour SN toi chose...
  - Revoir notre manière de mesurer la taille des speckles *Utiliser d'abord l'algorithme HiLo avant de faire la FFT de l'image?* ET *Utiliser la moyenne azimutale du spectre de puissance pour déterminer la grosseur moyenne des speckles (Voir Gabriel)*
  *Expérience prendre une image speckle, attendre 2 min, reprendre le même plan, attendre 2 min, reprendre le même plan...*
  - Expérience Vérifier le grossissement expérimental de l'illuminateur #onsaitquecestà5mm
  - Résolution axiale dépend de l'algorithme HiLo?
    *La résolution axiale d'un objectif est dépendante de sa résolution latérale.*
    *Plus petit objet pouvant être discernable par le système optique.*
    *Sectionnement optique ne doit pas être plus petit que la résolution axiale.* 
    *1 neurone = 4-5 um*
    
À discuter avec Dan :
  
  - Rergarder la grosseur des speckles avec la fibre à Bliq de NA = 0.63. *Hypothèse : Les speckles à la sortie de la fibre seront plus petits qu'avec la fibre de NA de 0.5 puisque le NA est plus grand MAIS la taille de la source au diffuseur sera plus grande puisque le NA de la fibre est plus grand. La combinaison des deux effets inverses doit être déterminée expérimentalement.* Taille théorique? *On pourrait obtenir la plus petite taille théoriqe...*
  - Voir Bertrand pour connecter le LSR (par LabJack) à Nirvana une fois que Steve Forest aura développé le circuit électronique pour éliminer le délai d'activation qui est actuellement de 600 ms.
  - Commander un autre objectif? *Une fois que les expérimentations concernant la discussion avec Bliq seront faites et analysées. En discuter avec Daniel*
      - Déterminer quels paramètres affectent la taille des speckles (NA, grossissement, Taille de la pupille d'entrée de l'objectif).
      - Déterminer quels paramètres affectent l'intensité du flickering (Taille des speckles, niveau de grit des diffuseurs).
  - Trouver une meilleure manière de générer de l'activité neuronale. (Solution odorante dans l'eau, installer des vis pour tenir le carré de verre dans lequel le poisson est placé, etc.)
  ______________________________________________________
   Discussion des speckles avec BLiq : 
 - NA de l'objectif change la taille des speckles sur les images? 
    - Expérience : Mesurer la taille des speckles sur un échantillon de FITC en utilisant 2 objectifs de même grossissement, mais avec des NA différents 
 - Grossissement objectif change la taille des speckles sur les images?
    - Expérience : Mesurer la taille des speckles sur un échantillon de FITC en utilisant 2 objectifs de même NA, mais avec des grossissements différents.
 - Back aperture de l'objectif change la taille des speckles sur les images?
    - Expérience : Comme le diamètre du back aperture de l'objectif varie en fonction du NA et du grossissement, son influence pourra être déduite à partir des deux dernières expériences. Par contre, il est important de s'assurer que le BA des objectifs utilisés lors des expériences sont remplis.
 - Taille plus petites des speckles diminue le flickering?
    - Expérience : Prendre des images d'un échantillon de FITC et de l'échantillon de cellules de rein de Bliq à l'aide d'une fibre de NA de 0.39, de 0.5 et de 0.63. Comparer le flickering observé sur chaque stack.
 - Nombre de grits du diffuseur change le flickering? Comment il le change?
    - Expérience : Prendre des images d'un échantillon de FITC et de l'échantillon de cellules de rein de Bliq à l'aide de diffuseurs de 120, 220 et 1500 grits. Tourner les diffuseurs lors de l'expérience pour observer du flickering. Comparer ensuite le flickering observé sur chaque stack.
    
