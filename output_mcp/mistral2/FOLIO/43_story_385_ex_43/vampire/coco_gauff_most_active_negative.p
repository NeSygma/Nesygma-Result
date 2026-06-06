fof(axiom_1, axiom, ! [X] : (highly_ranked_wta(X) => most_active_players(X))).
fof(axiom_2, axiom, ! [X] : ((at_event(X, roland_garros_2022) & lost_to(X, iga_swiatek)) => highly_ranked_wta(X))).
fof(axiom_3, axiom, ! [X] : (at_event(X, roland_garros_2022) & gender(X, female) => lost_to(X, iga_swiatek))).
fof(axiom_4, axiom, ! [X] : (at_event(X, roland_garros_2022) => (gender(X, female) | gender(X, male)))).
fof(axiom_5, axiom, ! [X] : ((at_event(X, roland_garros_2022) & gender(X, male)) => lost_to(X, rafael_nadal))).
fof(axiom_6, axiom, (highly_ranked_wta(coco_gauff) | lost_to(coco_gauff, rafael_nadal)) => ~gender(coco_gauff, male)).
fof(axiom_7, axiom, at_event(coco_gauff, roland_garros_2022)).
fof(goal_negation, conjecture, ~most_active_players(coco_gauff)).