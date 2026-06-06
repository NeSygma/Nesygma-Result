fof(categories, axiom, ! [X] : (ml_algorithm(X) => (supervised(X) | unsupervised(X) | reinforcement(X)))).
fof(unsupervised_no_labels, axiom, ! [X] : (unsupervised(X) => ~requires_labeled_data(X))).
fof(state_of_the_art_trained_with_ml, axiom, ? [X] : (state_of_the_art_summarization_model(model) & ml_algorithm(X) & trained_with_ml(model, X))).
fof(no_reinforcement_for_summarization, axiom, ! [X] : (state_of_the_art_summarization_model(model) & trained_with_ml(model, X) => ~reinforcement(X))).
fof(ml_for_summarization_requires_labels, axiom, ! [X] : (ml_algorithm(X) & ? [Model] : trained_with_ml(Model, Model) => requires_labeled_data(X))).

fof(conclusion, conjecture, ? [X] : (state_of_the_art_summarization_model(model) & supervised(X) & trained_with_ml(model, X))).