% Premise 1: Every NLP task is either a language generation or language understanding task
fof(premise_1, axiom, ! [X] : (nlp_task(X) => (language_generation(X) | language_understanding(X)))).

% Premise 2: If output is text sequence, then it's a language generation task
fof(premise_2, axiom, ! [X] : ((nlp_task(X) & output_is_text(X)) => language_generation(X))).

% Premise 3: Machine translation is an NLP task
fof(premise_3, axiom, nlp_task(machine_translation)).

% Premise 4: Output of machine translation is a text sequence
fof(premise_4, axiom, output_is_text(machine_translation)).

% Conclusion: Machine translation is a language understanding task
fof(goal, conjecture, language_understanding(machine_translation)).