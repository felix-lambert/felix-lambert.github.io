Source: https://www.youtube.com/watch?v=Y_XM3Bu-4yc

Machine learning

On pensait avant que l'intelligence était liée à une forme de raisonnement logique. On pensait que c'était une forme d'expression symbolique. On pensait que la pensée était une forme de langage logique simplifiée.

Mais on se rend compte de plus en plus que ce sont des activités de vecteurs neuronaux.

Est-ce qu'il y a un changement de paradigme ?

Oui parce que notre relation avec les machines peut changer. Au lieu de programmer les machines, on leur montre comment elles peuvent se programmer elles-mêmes. C'est une autre façon d'utiliser les machines. Le fait de programmer des machines va peut-être devenir obsolète.

Au niveau d'un programme informatique, on travaille avec des règles et des data pour générer des réponses.
En machine learning, on utilise des réponses et des data pour générer des règles. Donc en machine learning, il faut assembler un certains nombre de réponses de ce qu'on veut voir en input de sortie. C'est l'ordinateur qui trouve les règles derrières.

Le nouveau paradigme est d'avoir beaucoup d'exemples et des label pour ces exemples.

Qu'est ce que le deep learning ?

Le deep learning est le fait d'entraîner des réseaux de neurones.

Avec tenserflow on a par exemple:

```python
model = keras.Sequential([Keras.layers.Dense(units=1, input_shape=[1])])
```

Ici c'est écrit en python et appelle une api dans tensorflow qui s'appelle keras. Keras est une api qui permet de définir très facilement des réseaux de neurones.

Un réseau neuronal est une suite de fonctions qui peut apprendre des patterns. Le réseau neuronal le plus simple est un réseau neuronal avec simplement un seul neurone. C'est exactement ce qu'a le code ci-dessus. Avec Keras on "Dense" pour définir un "layer" de neurone connecté. Il y a simplement une unité ici donc un seul neurone.

```python
model = keras.Sequential([Keras.layers.Dense(units=1, input_shape=[1])])
model.compile(optimizer='sgd', loss='mean_squared_error')
```

Le réseau neuronal n'a aucune idée de la relation entre x (input) et y (output) donc il devine. La fonction "loss" utilise les data qu'elle connaît pour mesurer la qualité de la prédiction et donne cette information à "optimizer" qui devine la prochaine prédiction. La logique derrière est que chaque prédiction devrait être meilleure que la précédente.

```python
model = keras.Sequential([Keras.layers.Dense(units=1, input_shape=[1])])
model.compile(optimizer='sgd', loss='mean_squared_error')

xs = np.array([-1.0, 0.0, 1.0, 2.0, 3.0, 4.0], dtype=float)
ys = np.array([-3.0, -1.0, 1.0, 3.0, 5.0, 7.0], dtype=float)

```

"np.array" utilise une librarie python qui s'appelle "numpie" qui rend simple la représentation des data.

```python
model = keras.Sequential([Keras.layers.Dense(units=1, input_shape=[1])])
model.compile(optimizer='sgd', loss='mean_squared_error')

xs = np.array([-1.0, 0.0, 1.0, 2.0, 3.0, 4.0], dtype=float)
ys = np.array([-3.0, -1.0, 1.0, 3.0, 5.0, 7.0], dtype=float)

model.fit(xs, ys, epochs=500)

```

L'entraînement se produit dans la fonction "fit". On demande au modèle de deviner comment coordonner les valeurs x aux valeurs y. La valeur de epochs veut dire que ça va aller dans la boucle d'entraînement 500 fois.

La boucle fait la chose suivante: deviner, mesurer si elle a plutôt bien ou plutôt mal deviner, donner cette information à "optimizer" puis recommencer.

```python
model = keras.Sequential([Keras.layers.Dense(units=1, input_shape=[1])])
model.compile(optimizer='sgd', loss='mean_squared_error')

xs = np.array([-1.0, 0.0, 1.0, 2.0, 3.0, 4.0], dtype=float)
ys = np.array([-3.0, -1.0, 1.0, 3.0, 5.0, 7.0], dtype=float)

model.fit(xs, ys, epochs=500)

print(model.predict([10.0]))
```

Quand le modèle a fini de s'entraîner, il va nous donner des valeurs en utilisant la méthode "predict". Normalement predict devrait nous retourner 19 mais en réalité cette méthode nous retourne une valeur très proche de 19 mais pas exactement 19. Pourquoi ? Parce qu'on a entraîné le modèle en utilisant très peu de data. Il n'y a que 6 points linéaire. Aussi, le modèle utilise la probabilité.

Qu'est ce qu'on a besoin pour créer du deep learning ?

Beaucoup de data. Mais heureusement le phénomène de digitalisation permet aux utilisateurs de générer beaucoup de data, lorsqu'ils utilisent des outils numériques comme des smartphones, des ordinateurs ou des objets connectés. Donc pour qu'un algorithme de deep learning soit performant on a besoin de 2 choses:

1 il faut pouvoir entraîner un assez large réseau de neurones
2 il faut beaucoup de data
3 il faut une machine puissante CPU ou GPU

Une machine puissante permet de voir rapidement les résultats du réseau de neurone qu'on a entraîné.
Qu'est ce que le deep learning ?

Donc pour progresser en machine learning il faut entraîner beaucoup de data dans un large réseau de neurones sur une machine puissante. Avec de plus en plus de data et des machines de plus en plus puissantes, on devrait être de plus en plus performant en machine learning.

On a besoin d'un dataset

Exemple: des maisons avec des informations (le nombre de m2, le prix).

Le but est de prévoir le prix d'une maison en fonction de sa taille.

Pour faire ce modèle on a besoin d'un modèle de base de régression linéaire.

On a en entrée du réseau de neurone le nombre de m2 qui est x et le but est d'avoir en sortie le prix qui est y. Entre x et y on a un neurone qui implémente la fonction. On peut "stack" plusieurs neurones.

On peut aller plus loin en ajoutant le nombre de chambres, la localité, si on peut marcher facilement autour, la qualité des écoles... Tous ces paramètres peuvent encore plus nous aider à prédire le prix. Tous ces paramètres agrandissent notre réseau de neurones.

Donc on peut avoir en entrée:

la taille
le nombre de chambres
le zip code
la qualité de vie du quartier

Le but est de pouvoir prédire le prix. Tous les neurones prennent les 4 paramètres en entrée. On rentre des caractéristiques d'une maison et d'un quartier pour estimer (prévoir) le prix d'une maison.

Qu'est ce que la classification binaire ?

On a une image: 1 est un chat 0 n'est pas un chat. x est une image y va être la valeur de sortie.

Qu'est ce que la vectorisation ?

Ca permet de se débarrasser des boucles for dans notre code. Le but de la vectorisation est d'éviter d'attendre trop longtemps avant d'avoir un résultat. Les boucles for sur un modèle de machine learning prennent trop de temps, même avec une machine puissante. Donc le savoir-faire en machine learning est de réussir à vectoriser.

C'est la fonction np.dot qui permet de faire la vectorisation. Donc np.dot permet de faire notre computation beaucoup plus vite. C'est le cas pour des supports type GPU mais aussi pour les CPU. LE GPU a la réputation d'être encore plus rapide pour ces calculs que les CPU.

Exemple:

```python
import numpy as np
import time

a = np.array([1, 2, 3, 4])

print(a)

a = np.random.rand(1000000)
b = np.random.rand(1000000)

tic = time.time()

c = np.dot(a, b)

toc = time.time()

print(c)
print("Vectorized version: " + str(1000*(toc - tic)) + "ms")


c = 0
tic = time.time()

for i in range(1000000):
  c += a[i]*b[i]

toc = time.time()

print(c)
print("For loop version: " + str(1000*(toc - tic)) + "ms")
```

Ouput:
[1 2 3 4]
249980.66204718698
Vectorized version: 1.247406005859375ms
249980.66204718538
For loop version: 384.48429107666016ms

Donc quand c'est possible, il faut éviter d'utiliser les boucles for.

Maintenant un exemple concret.

On a une pomme, du boeuf, des oeufs, et des pommes de terre

La pomme a 56.0 calories de glucide, 1.2 de protéine, et 1.8 de graisse
Le boeuf a 0.0 calories de glucide, 104.0 de protéine et 135.0 de graisse
L'oeuf a 4.4 calories de glucide, 52.0 de protéine et 99.0 de graisse
La pomme de terre a 68.0 calories de glucide, 8.0 de protéine et 0.9 de graisse

Pour calculer le pourcentage moyen de tous ces ingrédients, on a pas besoin de faire de boucle for.

On peut faire:

```python
import numpy as np

# matrix de 3 sur 4 (3, 4)
A = np.array([[56.0, 0.0, 4.4, 68.0], [1.2, 104.0, 52.0, 8.0], [1.8, 135.0, 99.0, 0.9]])

print(A)

# axis=0 on veut que python de faire le calcul de haut en bas
# axis=1 le calcul se fera de gauche à droite
# La somme va devenir une matrix de 1, 4
cal = A.sum(axis=0)

print(cal)

# ici on n'a pas besoin d'appeler reshape parce que la matrix faire déjà est déjà 1 tableau de 4
# reshape est très rapide donc on peut le réutiliser souvent
percentage = 100 * A / cal.reshape(1,4)

print(percentage)
```

Output:
[[56.    0.    4.4  68. ]
 [  1.2 104.   52.    8. ]
 [  1.8 135.   99.    0.9]]
[ 59. 239. 155.4 76.9]
[[94.91525424  0.          2.83140283 88.42652796]
 [ 2.03389831 43.51464435 33.46203346 10.40312094]
 [ 3.05084746 56.48535565 63.70656371  1.17035111]]

Comment je fais pour comparer le niveau de similarité entre les ingrédients ?

J'utilise un environnement d'exécution Node.js pour les fonctions Firebase avec la bibliothèque TensorFlow.js pour exécuter des modèles TensorFlow dans un navigateur ou dans un environnement Node.js.

Puis je télécharge un modèle word2vec pré-entraîné sur codelab. Ensuite, j'utilise la bibliothèque TensorFlow.js pour charger le modèle dans une fonction Firebase Cloud. J'utilise la méthode tf.loadLayersModel() pour charger le modèle à partir de l'emplacement où il est stocké.

Avec python, je peux utiliser la méthode model.most_similar() qui est définie dans la bibliothèque Gensim. Toutefois, il ne peut pas être directement utilisé dans une fonction Firebase Cloud écrite en JavaScript. Je dois alos convertir le modèle TensorFlow entraîné en Python en un modèle TensorFlow.js en utilisant la commande tensorflowjs_converter qui est incluse dans le paquet TensorFlow.

Mon but est d'obtenir un comportement similaire à model.most_similar() avec TensorFlow.js, je vais devoir implémenter une logique similaire en utilisant les fonctionnalités de TensorFlow.js.

Voici donc les étapes

1 Charger le modèle TensorFlow.js en utilisant tf.loadLayersModel().

2 Préparer les données d'entrée pour le modèle en convertissant les mots en vecteurs de mots (word embeddings) en utilisant la couche d'embedding du modèle.

3 Exécuter le modèle en utilisant les données d'entrée pour obtenir les vecteurs de sortie pour chaque mot.

4 Calculez la similarité cosinus entre les vecteurs de sortie et le vecteur d'entrée pour le mot 'Feta'

5 Triez les résultats par ordre de similarité décroissante et renvoyez les N résultats les plus similaires

Il existe plusieurs méthodes pour calculer la similarité entre les vecteurs d'embeddings, mais l'une des plus couramment utilisées est la similarité cosinus.

Modèle

Dans tenserflow, il y a plusieurs modèles. On définit un modèle pour entraîner un nouveau modèle. Il est possible d'entraîner des modèles séparément et de les réutiliser dans le navigateur ou sur un serveur simplement en le testant.

Pour entraîner un nouveau modèle:

```javascript
// Définit un modèle pour la régression linéaire
const linearModel = tf.sequential();

// Va générer un shape de 1
linearModel.add(tf.layers.dense({ units: 1, inputShape: [1] }));

// Préparer le modèle pour l'entraînement
linearModel.compile({ loss: "meanSquaredError", optimizer: "sgd" });

// Entraînement
// Comme un tableau de chiffres
const xs = tf.tensor1d([6, 6, 8, 9]);

const ys = tf.tensor1d([1, 9, 7, 5]);

await linearModel.fit(xs, ys);

// Prévoir
const output = linearModel.predict(tf.tensor2d([val], [1, 1]));

const prediction = Array.from(output.dataSync())[0];

console.log(prediction);
```

Lorsqu'un modèle est entraîné. On peut le convertir en tensorflow.js et l'importer en utilisant tf.loadModal en javascript.

tf.sequential...

Il y a des layers.

Ce modèle a besoin d'être entraîné en lui rentrant des data. Ces data doivent être entraîné sous la forme du tensor. Le tensor peut prendre différentes dimensions. Un tensor d'une seule dimension est par exemple comme un simple tableau de chiffres.

Par convention on nomme le tensor qui entraîne x. Et le label de ce tensor est y. C'est y qu'on a envie de prévoir. Le tensor qu'on prédit va aussi nous retourner un nouveau tensor. Après on peut reconvertir ce tensor en data.

Le but du machine learning est de pouvoir prévoir le résultat de ce qui va arriver après.

# Tidy

tf.tidy empêche les fuites mémoires. En utilisant tidy on est sûr que tous les tensors sont libérés de la mémoire.

# Embedding

Le "embedding" est une représentation d'une donnée sous forme de tensor.
