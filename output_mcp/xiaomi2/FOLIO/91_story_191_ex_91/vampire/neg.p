fof(premise_1, axiom, ! [X] : (nlp_task(X) => (language_generation(X) | language_understanding(X)))).
fof(premise_2, axiom, ! [X] : (text_sequence_output(X) => language_generation(X))).
fof(premise_3, axiom, nlp_task(machine_translation)).
fof(premise_4, axiom, text_sequence_output(machine_translation)).
fof(goal, conjecture, ~language_generation(machine_translation)).