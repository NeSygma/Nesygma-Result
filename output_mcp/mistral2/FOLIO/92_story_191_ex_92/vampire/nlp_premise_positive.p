fof(all_nlp_tasks_are_gen_or_under, axiom, 
    ! [X] : (nlp_task(X) => (language_generation_task(X) | language_understanding_task(X)))).

fof(outputs_text_implies_gen, axiom, 
    ! [X] : ((nlp_task(X) & outputs_text_sequence(X)) => language_generation_task(X))).

fof(mt_is_nlp, axiom, nlp_task(machine_translation)).

fof(mt_outputs_text, axiom, outputs_text_sequence(machine_translation)).

fof(conclusion, conjecture, language_understanding_task(machine_translation)).