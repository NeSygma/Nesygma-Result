fof(premise_1, axiom, ! [X] : (nlp_task(X) => (generation_task(X) | understanding_task(X)))).
fof(premise_2, axiom, ! [X] : ((nlp_task(X) & output_is_text_sequence(X)) => generation_task(X))).
fof(premise_3, axiom, nlp_task(machine_translation)).
fof(premise_4, axiom, output_is_text_sequence(machine_translation)).
fof(conclusion, conjecture, generation_task(machine_translation)).