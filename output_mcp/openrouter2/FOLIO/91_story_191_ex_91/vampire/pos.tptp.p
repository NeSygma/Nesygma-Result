fof(premise1, axiom, ![T] : (nlp_task(T) => (language_generation(T) | language_understanding(T)))).
fof(premise2, axiom, ![T] : (output_is_text_sequence(T) => language_generation(T))).
fof(premise3, axiom, nlp_task(machine_translation)).
fof(premise4, axiom, output_is_text_sequence(machine_translation)).
fof(conjecture, conjecture, language_generation(machine_translation)).