% Positive version: conclusion "Unsupervised learning is used to train the model"
fof(premise_1, axiom, ! [X] : (ml_algorithm(X) => (category(X, supervised) | category(X, unsupervised) | category(X, reinforcement)))).
fof(premise_2, axiom, ! [X] : (category(X, unsupervised) => ~requires_labeled_data(X))).
fof(premise_3, axiom, ? [X] : (ml_algorithm(X) & trains_model(X))).
fof(premise_4, axiom, ! [X] : ((ml_algorithm(X) & trains_model(X)) => ~category(X, reinforcement))).
fof(premise_5, axiom, ! [X] : ((ml_algorithm(X) & trains_model(X)) => requires_labeled_data(X))).
fof(conclusion, conjecture, ? [X] : (ml_algorithm(X) & category(X, unsupervised) & trains_model(X))).