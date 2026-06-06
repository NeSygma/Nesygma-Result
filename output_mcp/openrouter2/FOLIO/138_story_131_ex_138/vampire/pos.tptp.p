fof(machine_learning_category, axiom, ! [A] : (machine_learning(A) => (category(A, supervised) | category(A, unsupervised) | category(A, reinforcement)))).
fof(unsupervised_no_labels, axiom, ! [A] : (category(A, unsupervised) => ~requires_labeled_data(A))).
fof(reinforcement_not_used, axiom, ! [A] : (category(A, reinforcement) => ~used_to_train(A, summarization_model))).
fof(used_to_train_is_ml, axiom, ! [A] : (used_to_train(A, summarization_model) => machine_learning(A))).
fof(used_to_train_requires_labels, axiom, ! [A] : (used_to_train(A, summarization_model) => requires_labeled_data(A))).
fof(exists_used_to_train, axiom, ? [A] : (machine_learning(A) & used_to_train(A, summarization_model))).
fof(conjecture, conjecture, ? [A] : (category(A, supervised) & used_to_train(A, summarization_model))).