fof(premise1a, axiom, ! [X] : (nlp_task(X) => (gen_task(X) | und_task(X)))).
fof(premise1b, axiom, ! [X] : ((gen_task(X) & und_task(X)) => $false)).
fof(premise2, axiom, ! [X] : ((nlp_task(X) & text_output(X)) => gen_task(X))).
fof(premise3, axiom, nlp_task(machine_translation)).
fof(premise4, axiom, text_output(machine_translation)).
fof(goal_neg, conjecture, ~gen_task(machine_translation)).