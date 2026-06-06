fof(axiom_1, axiom, ! [X] : (nlp_task(X) => (gen_task(X) | understand_task(X)))).
fof(axiom_2, axiom, ! [X] : ((nlp_task(X) & output_text_seq(X)) => gen_task(X))).
fof(axiom_3, axiom, nlp_task(machine_translation)).
fof(axiom_4, axiom, output_text_seq(machine_translation)).
fof(conjecture, conjecture, gen_task(machine_translation)).