fof(categorization, axiom,
    ! [X] : (is_nlp_task(X) => (is_gen_task(X) | is_understand_task(X)))).

fof(output_text_implies_gen, axiom,
    ! [X] : ((is_nlp_task(X) & has_output_text_sequence(X)) => is_gen_task(X))).

fof(mt_is_nlp, axiom,
    is_nlp_task(machine_translation)).

fof(mt_has_text_output, axiom,
    has_output_text_sequence(machine_translation)).

fof(conclusion_negation, conjecture,
    ~is_gen_task(machine_translation)).