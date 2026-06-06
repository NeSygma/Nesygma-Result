% Positive version: original claim as conjecture
% Premises:
% 1. Diamond Mine is a professional wrestling stable formed in WWE.
fof(premise_1, axiom, stable(diamond_mine)).
fof(premise_1b, axiom, formed_in_wwe(diamond_mine)).

% 2. Roderick Strong leads Diamond Mine.
fof(premise_2, axiom, leads(roderick_strong, diamond_mine)).

% 3. Diamond Mine includes the Creed Brothers and Ivy Nile.
fof(premise_3, axiom, includes(diamond_mine, creed_brothers)).
fof(premise_3b, axiom, includes(diamond_mine, ivy_nile)).

% 4. Imperium has a feud with Diamond Mine.
fof(premise_4, axiom, feud(imperium, diamond_mine)).

% Distinct entities
fof(distinct, axiom, (roderick_strong != diamond_mine & roderick_strong != creed_brothers & roderick_strong != ivy_nile & roderick_strong != imperium & diamond_mine != creed_brothers & diamond_mine != ivy_nile & diamond_mine != imperium & creed_brothers != ivy_nile & creed_brothers != imperium & ivy_nile != imperium)).

% Conclusion: Roderick Strong leads the Creed Brothers.
fof(goal, conjecture, leads(roderick_strong, creed_brothers)).