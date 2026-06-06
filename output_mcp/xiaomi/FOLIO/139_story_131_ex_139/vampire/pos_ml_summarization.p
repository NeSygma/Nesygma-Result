fof(ml_categories, axiom,
    (ml_category(supervised_learning) &
     ml_category(unsupervised_learning) &
     ml_category(reinforcement_learning))).

fof(unsupervised_no_labels, axiom,
    ! [X] : (ml_category(X) & X = unsupervised_learning => ~requires_labeled_data(X))).

fof(summarization_uses_ml, axiom,
    ? [X] : (ml_category(X) & used_to_train(X, text_summarization_model))).

fof(reinforcement_not_used, axiom,
    ~used_to_train(reinforcement_learning, text_summarization_model)).

fof(summarization_needs_labels, axiom,
    ! [X] : ((ml_category(X) & used_to_train(X, text_summarization_model)) => requires_labeled_data(X))).

fof(distinct_categories, axiom,
    (supervised_learning != unsupervised_learning &
     supervised_learning != reinforcement_learning &
     unsupervised_learning != reinforcement_learning)).

fof(goal, conjecture,
    used_to_train(unsupervised_learning, text_summarization_model)).