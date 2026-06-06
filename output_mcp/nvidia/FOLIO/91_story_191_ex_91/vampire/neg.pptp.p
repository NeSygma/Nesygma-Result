fof(axiom1, axiom, ! [X] : (nlp_task(X) => (lg_task(X) | lu_task(X))).
fof(axiom2, axiom, ! [X] : ((nlp_task(X) & output_is_text(X)) => lg_task(X))).
fof(axiom3, axiom, nlp_task(mt)).
fof(axiom4, axiom, output_is_text(mt)).
fof(conjecture, conjecture, ~lg_task(mt)).