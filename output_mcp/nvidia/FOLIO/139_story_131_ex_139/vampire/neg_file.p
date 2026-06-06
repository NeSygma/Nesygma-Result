fof(categorization, axiom, ! [M] : (trains_with(text_summarization_model, M) => (M = supervised_learning | M = unsupervised_learning | M = reinforcement_learning))).
fof(unsupervised_no_labeled, axiom, ~requires_labeled_data(unsupervised_learning)).
fof(reinforcement_not_used, axiom, ~trains_with(text_summarization_model, reinforcement_learning)).
fof(training_requires_labeled, axiom, ! [M] : (trains_with(text_summarization_model, M) => requires_labeled_data(M))).
fof(goal, conjecture, ~trains_with(text_summarization_model, unsupervised_learning)).