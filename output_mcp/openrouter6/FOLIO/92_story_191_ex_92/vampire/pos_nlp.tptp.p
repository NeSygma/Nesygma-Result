fof(premise1, axiom, ! [X] : (nlp_task(X) => (generation_task(X) | understanding_task(X)))).
fof(premise2, axiom, ! [X] : ((nlp_task(X) & output_is_text_sequence(X)) => generation_task(X))).
fof(premise3, axiom, nlp_task(machine_translation)).
fof(premise4, axiom, output_is_text_sequence(machine_translation)).
fof(goal, conjecture, understanding_task(machine_translation)).