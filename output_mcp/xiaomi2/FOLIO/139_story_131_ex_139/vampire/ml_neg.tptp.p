fof(supervised_is_ml, axiom, ml_algorithm(supervised)).
fof(unsupervised_is_ml, axiom, ml_algorithm(unsupervised)).
fof(reinforcement_is_ml, axiom, ml_algorithm(reinforcement)).
fof(distinct_categories, axiom, (supervised != unsupervised & supervised != reinforcement & unsupervised != reinforcement)).
fof(categories_exhaustive, axiom, ! [X] : (ml_algorithm(X) => (X = supervised | X = unsupervised | X = reinforcement))).
fof(unsupervised_no_labels, axiom, ~requires_labeled_data(unsupervised)).
fof(summarization_trained, axiom, ? [X] : (ml_algorithm(X) & trains(X, summarization_model))).
fof(not_reinforcement, axiom, ~trains(reinforcement, summarization_model)).
fof(summarization_needs_labels, axiom, ! [X] : (trains(X, summarization_model) => requires_labeled_data(X))).
fof(goal, conjecture, ~trains(unsupervised, summarization_model)).