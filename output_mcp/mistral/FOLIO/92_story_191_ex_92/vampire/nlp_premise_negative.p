fof(premise_1, axiom, ! [X] : (nlp_task(X) => (generation_task(X) | understanding_task(X)))).
fof(premise_2, axiom, ! [X] : ((nlp_task(X) & has_text_output(X)) => generation_task(X))).
fof(premise_3, axiom, nlp_task(machine_translation)).
fof(premise_4, axiom, has_text_output(machine_translation)).
fof(goal_negation, conjecture, ~understanding_task(machine_translation)).