fof(premise1, axiom, ! [T] : (nlp_task(T) => (lang_gen_task(T) | lang_under_task(T)))).
fof(premise2, axiom, ! [T] : ((nlp_task(T) & output_is_text_sequence(T)) => lang_gen_task(T))).
fof(premise3, axiom, nlp_task(machine_translation)).
fof(premise4, axiom, output_is_text_sequence(machine_translation)).
fof(conjecture, conjecture, ~lang_under_task(machine_translation)).