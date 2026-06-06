fof(ax1, axiom, ! [T] : (nlp_task(T) => (gen(T) | und(T)))).
fof(ax2, axiom, ! [T] : ((nlp_task(T) & output_text(T)) => gen(T))).
fof(fact1, axiom, nlp_task(mt)).
fof(fact2, axiom, output_text(mt)).
fof(goal, conjecture, und(mt)).