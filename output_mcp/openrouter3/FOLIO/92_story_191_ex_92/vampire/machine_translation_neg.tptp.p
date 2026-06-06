% Negative version: Machine translation is NOT a language understanding task
fof(premise_1, axiom, ! [X] : (nlp_task(X) => (generation_task(X) | understanding_task(X)))).
fof(premise_2, axiom, ! [X] : (has_output(X, text_sequence) => generation_task(X))).
fof(premise_3, axiom, nlp_task(machine_translation)).
fof(premise_4, axiom, has_output(machine_translation, text_sequence)).
fof(conclusion, conjecture, ~understanding_task(machine_translation)).