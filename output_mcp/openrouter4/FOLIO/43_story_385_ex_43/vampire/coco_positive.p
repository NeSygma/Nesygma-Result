% Positive file: conjecture is most_active(coco)
fof(premise1, axiom, ! [X] : (ranked_highly(X) => most_active(X))).
fof(premise2, axiom, ! [X] : (lost_to_iga(X) => ranked_highly(X))).
fof(premise3, axiom, ! [X] : (female_at_rg(X) => lost_to_iga(X))).
fof(premise4, axiom, ! [X] : (player_at_rg(X) => (female_at_rg(X) | male_at_rg(X)))).
fof(premise5, axiom, ! [X] : (male_at_rg(X) => lost_to_nadal(X))).
fof(premise6, axiom, ((ranked_highly(coco) | lost_to_nadal(coco)) => ~male_at_rg(coco))).
fof(premise7, axiom, player_at_rg(coco)).
fof(goal, conjecture, most_active(coco)).