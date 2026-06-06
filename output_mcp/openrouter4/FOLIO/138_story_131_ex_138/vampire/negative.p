fof(p1, axiom, ! [X] : (ml_alg(X) => (supervised(X) | unsupervised(X) | reinforcement(X)))).
fof(p2, axiom, ! [X] : (unsupervised(X) => ~requires_labeled(X))).
fof(p3, axiom, ? [X] : (ml_alg(X) & trains(X, sota_model))).
fof(p4, axiom, ! [X] : (trains(X, sota_model) => ~reinforcement(X))).
fof(p5, axiom, ! [X, M] : ((ml_alg(X) & trains(X, M) & text_summarization(M)) => requires_labeled(X))).
fof(f1, axiom, text_summarization(sota_model)).
fof(goal, conjecture, ~? [X] : (supervised(X) & trains(X, sota_model))).