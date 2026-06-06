% Negative version: negated claim as conjecture
fof(premise_1, axiom, professional_wrestling_stable(diamond_mine)).
fof(premise_2, axiom, leads(roderick_strong, diamond_mine)).
fof(premise_3, axiom, includes(diamond_mine, creed_brothers)).
fof(premise_4, axiom, includes(diamond_mine, ivy_nile)).
fof(premise_5, axiom, feud(imperium, diamond_mine)).

fof(distinct, axiom, (roderick_strong != diamond_mine & roderick_strong != creed_brothers & roderick_strong != ivy_nile & roderick_strong != imperium & diamond_mine != creed_brothers & diamond_mine != ivy_nile & diamond_mine != imperium & creed_brothers != ivy_nile & creed_brothers != imperium & ivy_nile != imperium)).

% Negated conclusion: It is NOT the case that Roderick Strong leads a professional wrestling stable.
% i.e., for all S, if S is a professional wrestling stable then Roderick Strong does NOT lead S.
fof(goal_neg, conjecture, ~? [S] : (professional_wrestling_stable(S) & leads(roderick_strong, S))).