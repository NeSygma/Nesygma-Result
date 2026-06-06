fof(task_type, axiom, ! [X] : (task(X) => (generation(X) | understanding(X)))).
fof(xor_constraint, axiom, ! [X] : (task(X) => ~(generation(X) & understanding(X)))).
fof(gen_rule, axiom, ! [X] : (output_text(X) => generation(X))).
fof(mt_is_task, axiom, task(mt)).
fof(mt_output, axiom, output_text(mt)).
fof(goal, conjecture, understanding(mt)).