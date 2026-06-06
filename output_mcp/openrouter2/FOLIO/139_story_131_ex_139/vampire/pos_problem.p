fof(category, axiom, ! [X] : (ml_algorithm(X) => (supervised(X) | unsupervised(X) | reinforcement(X)))).
fof(unsup_no_label, axiom, ! [X] : (unsupervised(X) => ~requires_labeled_data(X))).
fof(exists_algo, axiom, ? [A] : (trained_with(model_sota, A) & ml_algorithm(A))).
fof(reinforce_not_used, axiom, ! [X] : (reinforcement(X) => ~trained_with(model_sota, X))).
fof(used_requires_label, axiom, ! [X] : ((ml_algorithm(X) & trained_with(model_sota, X)) => requires_labeled_data(X))).
fof(goal, conjecture, ? [X] : (unsupervised(X) & trained_with(model_sota, X))).