fof(premise1, axiom, ! [X] : (nlp_task(X) => (lang_gen(X) | lang_under(X)))).
fof(premise2, axiom, ! [X] : ((nlp_task(X) & output_text(X)) => lang_gen(X))).
fof(premise3, axiom, nlp_task(mt)).
fof(premise4, axiom, output_text(mt)).
fof(conclusion, conjecture, lang_under(mt)).