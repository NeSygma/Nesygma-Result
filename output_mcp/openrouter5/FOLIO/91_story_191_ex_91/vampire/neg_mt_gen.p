% Negative version: negated claim as conjecture
% Premises:
% 1. A natural language processing task can be categorized as either a language generation task or a language understanding task.
fof(premise1, axiom, ! [X] :
    (nlp_task(X) => (lang_gen_task(X) | lang_und_task(X)))).

% 2. If the output of a natural language processing task is a text sequence, then it is a language generation task.
fof(premise2, axiom, ! [X] :
    ((nlp_task(X) & output_text_seq(X)) => lang_gen_task(X))).

% 3. Machine translation is a natural language processing task.
fof(premise3, axiom, nlp_task(machine_translation)).

% 4. The output of machine translation is a text sequence.
fof(premise4, axiom, output_text_seq(machine_translation)).

% Negated conclusion: Machine translation is NOT a language generation task.
fof(neg_conclusion, conjecture, ~lang_gen_task(machine_translation)).