fof(dm_stable, axiom, pw_stable(diamond_mine)).
fof(strong_leads, axiom, leads(roderick_strong, diamond_mine)).
fof(dm_includes_cb, axiom, includes(diamond_mine, creed_brothers)).
fof(dm_includes_in, axiom, includes(diamond_mine, ivy_nile)).
fof(imperium_feud, axiom, feud(imperium, diamond_mine)).

fof(distinct, axiom, (
    diamond_mine != roderick_strong &
    diamond_mine != creed_brothers &
    diamond_mine != ivy_nile &
    diamond_mine != imperium &
    roderick_strong != creed_brothers &
    roderick_strong != ivy_nile &
    roderick_strong != imperium &
    creed_brothers != ivy_nile &
    creed_brothers != imperium &
    ivy_nile != imperium
)).

% Negation of conclusion: Imperium DOES have a feud with a pw_stable that includes Ivy Nile
fof(goal, conjecture, ? [X] : (pw_stable(X) & includes(X, ivy_nile) & feud(imperium, X))).