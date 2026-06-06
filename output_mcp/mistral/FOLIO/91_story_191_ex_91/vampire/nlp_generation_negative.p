fof(categorization, axiom, ! [X] : (nlp_task(X) => (language_generation_task(X) | language_understanding_task(X)))).
fof(output_text_implies_generation, axiom, ! [X] : ((nlp_task(X) & has_output_text_sequence(X)) => language_generation_task(X))).
fof(machine_translation_is_nlp, axiom, nlp_task(machine_translation)).
fof(machine_translation_has_text_output, axiom, has_output_text_sequence(machine_translation)).
fof(conclusion_negation, conjecture, ~language_generation_task(machine_translation)).