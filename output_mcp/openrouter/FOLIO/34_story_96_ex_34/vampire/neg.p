% Negative version (negated conjecture)
fof(distinct_consts, axiom, (diamond_mine != roderick_strong & diamond_mine != creed_brothers & diamond_mine != ivy_nile & diamond_mine != imperium & roderick_strong != creed_brothers & roderick_strong != ivy_nile & roderick_strong != imperium & creed_brothers != ivy_nile & creed_brothers != imperium & ivy_nile != imperium)).

fof(prof_stable, axiom, professional_wrestling_stable(diamond_mine)).
fof(leads_fact, axiom, leads(roderick_strong, diamond_mine)).
fof(rule_leads_prof, axiom, ! [P,S] : ((leads(P,S) & professional_wrestling_stable(S)) => leads_prof_wrestling_stable(P))).

fof(goal_neg, conjecture, ~leads_prof_wrestling_stable(roderick_strong)).