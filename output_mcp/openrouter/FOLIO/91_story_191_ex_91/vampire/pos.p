fof(premise1, axiom, ! [T] : (nlp_task(T) => (gen(T) | understand(T)))).
fof(premise2, axiom, ! [T] : (output_text_seq(T) => gen(T))).
fof(premise3, axiom, nlp_task(machine_translation)).
fof(premise4, axiom, output_text_seq(machine_translation)).
fof(goal, conjecture, gen(machine_translation)).