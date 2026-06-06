% Positive version: Original conclusion as conjecture
fof(premise1, axiom, ! [X] : (ranked_high(X) => most_active(X))).
fof(premise2, axiom, ! [X] : (lost_to_iga(X) => ranked_high(X))).
fof(premise3, axiom, ! [X] : (female(X) => lost_to_iga(X))).
fof(premise4, axiom, ! [X] : (at_roland_garros(X) => (female(X) | male(X)))).
fof(premise5, axiom, ! [X] : (male(X) => lost_to_rafael(X))).
fof(premise6, axiom, (ranked_high(coco_gauff) | lost_to_rafael(coco_gauff)) => ~male(coco_gauff)).
fof(premise7, axiom, at_roland_garros(coco_gauff)).
fof(conclusion, conjecture, ~(lost_to_iga(coco_gauff) & most_active(coco_gauff))).