% Negative version: negated conclusion as conjecture
% Premises:
% 1. Diamond Mine is a professional wrestling stable formed in WWE.
fof(premise_1, axiom, professional_wrestling_stable(diamond_mine)).
fof(premise_1b, axiom, formed_in_wwe(diamond_mine)).

% 2. Roderick Strong leads Diamond Mine.
fof(premise_2, axiom, leads(roderick_strong, diamond_mine)).

% 3. Diamond Mine includes the Creed Brothers and Ivy Nile.
fof(premise_3, axiom, includes(diamond_mine, creed_brothers)).
fof(premise_3b, axiom, includes(diamond_mine, ivy_nile)).

% 4. Imperium has a feud with Diamond Mine.
fof(premise_4, axiom, feud(imperium, diamond_mine)).

% Distinctness
fof(distinct, axiom, (diamond_mine != imperium & diamond_mine != roderick_strong & diamond_mine != creed_brothers & diamond_mine != ivy_nile & imperium != roderick_strong & imperium != creed_brothers & imperium != ivy_nile & roderick_strong != creed_brothers & roderick_strong != ivy_nile & creed_brothers != ivy_nile)).

% Negated conclusion: Imperium DOES have a feud with a professional wrestling stable that includes Ivy Nile.
% i.e., There exists a stable S such that: professional_wrestling_stable(S) & includes(S, ivy_nile) & feud(imperium, S).
fof(goal_neg, conjecture, ? [S] : (professional_wrestling_stable(S) & includes(S, ivy_nile) & feud(imperium, S))).