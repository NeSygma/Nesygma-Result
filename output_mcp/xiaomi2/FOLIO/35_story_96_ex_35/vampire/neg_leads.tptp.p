fof(diamond_mine_is_stable, axiom, stable(diamond_mine)).
fof(strong_leads_dm, axiom, leads(roderick_strong, diamond_mine)).
fof(dm_includes_creed, axiom, includes(diamond_mine, creed_brothers)).
fof(dm_includes_ivy, axiom, includes(diamond_mine, ivy_nile)).
fof(imperium_feud_dm, axiom, feud(imperium, diamond_mine)).

fof(distinct_constants, axiom, (
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

fof(goal, conjecture, ~leads(roderick_strong, creed_brothers)).