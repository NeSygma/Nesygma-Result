fof(nlp_either_gen_or_understand, axiom,
    ! [X] : (nlp_task(X) => ((gen_task(X) | understand_task(X)) & ~(gen_task(X) & understand_task(X))))).

fof(text_output_implies_gen, axiom,
    ! [X] : ((nlp_task(X) & output_text(X)) => gen_task(X))).

fof(mt_is_nlp, axiom, nlp_task(mt)).

fof(mt_output_text, axiom, output_text(mt)).

fof(goal, conjecture, ~understand_task(mt)).