% Negative conjecture: unsupervised learning is NOT used to train the model
fof(unsup_no_label, axiom, ![A] : (unsupervised(A) => ~requires_labeled_data(A))).
fof(exist_alg, axiom, ?[A] : (used_to_train(A, model_ts) & ml_algorithm(A))).
fof(no_reinf, axiom, ![A] : (used_to_train(A, model_ts) => ~reinforcement(A))).
fof(req_label, axiom, ![A] : (used_to_train(A, model_ts) => requires_labeled_data(A))).
fof(goal, conjecture, ![A] : (unsupervised(A) => ~used_to_train(A, model_ts))).