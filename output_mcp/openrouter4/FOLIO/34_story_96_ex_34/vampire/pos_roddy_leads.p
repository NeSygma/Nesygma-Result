% Problem: Does Roderick Strong lead a professional wrestling stable?
% Positive version: original claim as conjecture

fof(premise_1, axiom, professional_wrestling_stable(diamond_mine)).
fof(premise_2, axiom, leads(roderick_strong, diamond_mine)).
fof(premise_3, axiom, includes(diamond_mine, creed_brothers) & includes(diamond_mine, ivy_nile)).
fof(premise_4, axiom, has_feud(imperium, diamond_mine)).

fof(goal, conjecture, ? [X] : (professional_wrestling_stable(X) & leads(roderick_strong, X))).