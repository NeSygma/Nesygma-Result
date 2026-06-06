fof(ml_supervised, axiom, ! [X] : (supervised(X) => ml_algorithm(X))).
fof(ml_unsupervised, axiom, ! [X] : (unsupervised(X) => ml_algorithm(X))).
fof(ml_reinforcement, axiom, ! [X] : (reinforcement(X) => ml_algorithm(X))).
fof(ml_exhaustive, axiom, ! [X] : (ml_algorithm(X) => (supervised(X) | unsupervised(X) | reinforcement(X)))).
fof(mutual_excl_1, axiom, ! [X] : (supervised(X) => ~unsupervised(X))).
fof(mutual_excl_2, axiom, ! [X] : (supervised(X) => ~reinforcement(X))).
fof(mutual_excl_3, axiom, ! [X] : (unsupervised(X) => ~reinforcement(X))).
fof(premise_2, axiom, ! [X] : (unsupervised(X) => ~requires_labeled_data(X))).
fof(premise_3, axiom, ? [X] : (ml_algorithm(X) & used_to_train(X, sota_tsm))).
fof(premise_4, axiom, ! [X] : (reinforcement(X) => ~used_to_train(X, sota_tsm))).
fof(premise_5, axiom, ! [X] : ((ml_algorithm(X) & used_to_train(X, sota_tsm)) => requires_labeled_data(X))).
fof(goal_neg, conjecture, ~? [X] : (supervised(X) & used_to_train(X, sota_tsm))).