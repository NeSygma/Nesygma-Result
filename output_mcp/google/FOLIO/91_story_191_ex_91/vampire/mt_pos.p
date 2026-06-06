fof(nlp_task_def, axiom, ! [T] : (nlp_task(T) => (lg_task(T) | lu_task(T)))).
fof(lg_rule, axiom, ! [T] : ((nlp_task(T) & output_is_text_sequence(T)) => lg_task(T))).
fof(mt_is_nlp, axiom, nlp_task(machine_translation)).
fof(mt_output, axiom, output_is_text_sequence(machine_translation)).
fof(goal, conjecture, lg_task(machine_translation)).