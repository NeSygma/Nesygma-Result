fof(premise1_exhaustive, axiom, ! [X] : (nlp_task(X) => (language_generation(X) | language_understanding(X)))).
fof(premise1_exclusive, axiom, ! [X] : (nlp_task(X) => (~language_generation(X) | ~language_understanding(X)))).
fof(premise2, axiom, ! [X] : ((nlp_task(X) & text_sequence_output(X)) => language_generation(X))).
fof(premise3, axiom, nlp_task(machine_translation)).
fof(premise4, axiom, text_sequence_output(machine_translation)).
fof(conclusion_neg, conjecture, ~language_understanding(machine_translation)).