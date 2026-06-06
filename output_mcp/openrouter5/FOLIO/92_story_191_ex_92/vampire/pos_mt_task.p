% Positive file: original claim as conjecture
% Premises:
% 1. A natural language processing task can be categorized as either a language generation task or a language understanding task.
fof(premise1, axiom, ! [X] : (nlp_task(X) => (generation_task(X) | understanding_task(X)))).
% 2. If the output of a natural language processing task is a text sequence, then it is a language generation task.
fof(premise2, axiom, ! [X] : ((nlp_task(X) & text_output(X)) => generation_task(X))).
% 3. Machine translation is a natural language processing task.
fof(premise3, axiom, nlp_task(machine_translation)).
% 4. The output of machine translation is a text sequence.
fof(premise4, axiom, text_output(machine_translation)).

% Conclusion: Machine translation is a language understanding task.
fof(goal, conjecture, understanding_task(machine_translation)).