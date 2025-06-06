Exercice CAR

On souhaite simuler une course entre 4 voitures. Voici les éléments qui composent une voiture : le nombre de litre
d'essence son nombre de kilomètres parcouru l'état de crevaison des pneus (on cherche à savoir si les pneus sont crevés)
la couleur de la voiture sa place dans le classement

Voici les spécifications de chaque voiture : Voiture bleue : commence la course avec 5 litres d'essences, n'a pas les
pneus crevés, et commence à la position n°4 au km 0. Voiture verte : commence la course avec 7 litres d'essences, n'a
pas les pneus crevés, et commence à la position n°3 au km 0. Voiture jaune : commence la course avec 3 litres
d'essences, n'a pas les pneus crevés, et commence à la position n°2 au km 0. Voiture rouge : commence la course avec 10
litres d'essences, n'a pas les pneus crevés, et commence à la position n°1 au km 0.

Lorsqu'une voiture roule, elle fait "VROUUUUUUM" suivit de la couleur de la voiture (afficher dans la console), consomme
1 litre d'essence, et avance de 10 km. De plus, une voiture a 1 chance sur 5 de ne pas consommer d'essence lorsqu'elle
roule, et elle a également 1 chance sur 20 de crever ses pneus.

Si une voiture a les pneus crevés ou si elle n'a plus d'essence, elle ne peut plus avancer. Une voiture a 1 chance sur 3
que ses pneus se réparent s'ils sont crevés, et elle a 1 chance sur 8 de récupérer 2 litres d'essence si la voiture n'a
plus d'essences. Le nombre de litre d'essence ne peut pas avoir de valeur négative : sa valeur minimum est 0. La course
fait un total de 100 km. Lorsqu'une voiture dépasse l'arrivée, la course s'arrête.

Lors de la course, des événements peuvent survenir : une voiture dépasse une autre voiture en nombre de kilomètre. Leurs
places dans le classement sont donc interverties. une voiture percute au hasard une autre voiture, à hauteur de 1 chance
sur 4 si la distance entre les deux voitures est inférieure ou égale à 10. Le nombre de km d'avancement des deux
véhicules sera divisé par 2 la prochaine fois que les deux voitures vont rouler. Après avoir dépassé la moitié des
kilomètres du parcours, une voiture peut déclencher un turbo et avancer du double de kilomètre la prochaine fois qu'elle
roulera. Dans ce cas, la voiture consomme 2 fois plus d'essence, et les pneus ne pourront pas être crevés.

On affiche les éléments suivants dans la console : une voiture n'a plus d'essence : on indique la couleur de la voiture
suivi de "n'a plus d'essence" une voiture a les pneus crevés : on indique la couleur de la voiture suivi de "a crevé ses
pneus" une voiture a de nouveau de l'essence : on indique la couleur de la voiture suivi de "a fait le plein d'essence"
une voiture a regonflé ses pneus : on indique la couleur de la voiture suivi de "a regonflé ses pneus" une voiture
déclenche un turbo : on indique la couleur de la voiture suivi de "appuie sur le champignon" une voiture double une
autre voiture : on indique quelle couleur de voiture dépasse quelle autre couleur de voiture. une voiture percute une
autre voiture : on indique quelle couleur de voiture percute quelle autre couleur de voiture. une voiture termine la
course : on affiche le classement de toutes les voitures suivit de leur couleur respective, suivit de leur nombre de km
parcouru.