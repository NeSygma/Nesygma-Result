fof(pref1, axiom, ! [X] : (rabbit(X) & spotted_campus(X)) => cute(X)).
fof(pref2, axiom, ? [X] : (turtle(X) & spotted_campus(X)).
fof(pref3, axiom, ! [X] : (spotted_campus(X)) => (rabbit(X) | squirrel(X)).
fof(pref4, axiom, ! [X] : skittish(X) => ~calm(X)).
fof(pref5, axiom, ! [X] : (squirrel(X) & spotted_campus(X)) => skittish(X)).
fof(fact_rockie_spotted, axiom, spotted_campus(rockie)).
fof(fact_rockie_calm, axiom, calm(rockie)).
fof(neg_goal, conjecture, (cute(rockie) & calm(rockie)) & ~(skittish(rockie) & turtle(rockie))).