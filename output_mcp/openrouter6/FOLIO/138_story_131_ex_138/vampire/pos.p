fof(axiom1, axiom, ! [X] : (ml_algorithm(X) => (supervised_learning(X) | unsupervised_learning(X) | reinforcement_learning(X)))).
fof(axiom2, axiom, ! [X] : (unsupervised_learning(X) => ~requires_labeled_data(X))).
fof(axiom3, axiom, ? [X] : (ml_algorithm(X) & trains_model(X, sota_model))).
fof(axiom4, axiom, ! [X] : (reinforcement_learning(X) => ~trains_model(X, sota_model))).
fof(axiom5, axiom, ? [X] : (ml_algorithm(X) & trains_model(X, sota_model) & requires_labeled_data(X))).
fof(goal, conjecture, ? [X] : (supervised_learning(X) & trains_model(X, sota_model))).