### Points non développés / non achevés

* Non implémenté :
  * gestion de plusieurs piles : dans l'implémentation actuelle, j'ai considéré
que nous avons une seule pile et que toutes les opérations sont faites au niveau
de cette pile.

* Non achevé :
  * amélioration de la documentation :
    * actuellement, il faut cliquer sur les requêtes pour pouvoir voir la
description. Ce serait bien de faire en sorte que la description soit visible
à l'extérieur de cette section.
    * dans les exemples pour le champ `StackItem.value`, on a `"string"` qui 
est un mauvais exemple. Effectivement, la valeur attendue est sous format
string, mais c'est une valeur numérique qui est attendue, corriger cela.
  * amélioration de l'API :
    * nettoyage de la pile : actuellement, la requête pour cette fonctionnalité
est un `DELETE /api/rpn/stack_items/clear`. Je pense qu'il serait peut-être plus
propre d'avoir plutôt un `DELETE /api/rpn/stack_items` (sans le suffixe `/clear`).
    * au niveau des objets retournés, afficher des identifiants qui permettent 
de décompter les éléments retournés plutôt que les `id` de la db. Par exemple, 
si on ajoute un élément et qu'on le supprime, on aura au niveau du premier
élément `id: 2`, on voudrait plutôt avoir `position: 1` ou simplement
supprimer ce champ vu que les données sont déjà rangées par ordre de création
  * tests
    * confirmer dans le test de récupération des éléments de la pile que les
données sont rangées par ordre de création
    * installer le package `coverage` et ajouter la mesure de la couverture de
code à la commande d'exécution des tests dans le `README`
  * au niveau du code
    * il y a la classe `StackOperationSerializer` qui a été utilisée pour 
faciliter la gestion d'erreurs sur les opérations, mais elle hérite de méthodes
abstraites `create` et `update` qu'elle n'utilise pas, à revoir
    * voir si on peut faire plus propre qu'aligner des "`if`" pour le support des
différentes opérations au niveau de `StackItemManager.perform_operation`
    * au niveau de `StackItemViewSet`, ça semble un peu maladroit d'ajouter
les méthodes `create` et `list` juste pour pouvoir mettre leurs descriptions. Il
y a un package `drf-spectacular` qui résout le problème de manière plus propre. 
Intégrer ce package ou voir comment c'est fait et reproduire si pas compliqué.
