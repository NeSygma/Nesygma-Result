% Machine Learning categories
fof(category, axiom, ! [X] : (ml_algorithm(X) => (supervised(X) | unsupervised(X) | reinforcement(X)))).

% Unsupervised learning does not require labeled data
fof(unsupervised_no_labeled, axiom, ! [X] : (unsupervised(X) => ~requires_labeled(X))).

% The state-of-the-art text summarization model is trained with machine learning algorithms
fof(fact_trained_ml, axiom, trained_with_ml(summarization_model)).

% Reinforcement learning is not used to train the state-of-the-art text summarization model
fof(no_reinforcement, axiom, ~reinforcement_used(summarization_model)).

% The Machine Learning algorithm for training text summarization models requires labeled data
fof(fact_alg_ml, axiom, ml_algorithm(alg_for_text_summarization)).
fof(fact_alg_trains, axiom, trains(alg_for_text_summarization, summarization_model)).
fof(fact_alg_requires_labeled, axiom, requires_labeled(alg_for_text_summarization)).

% Distinctness of the summarization model and the training algorithm
fof(distinct_constants, axiom, summarization_model != alg_for_text_summarization).

% If a supervised algorithm trains the summarization model, then supervised learning is used to train it
fof(axiom_supervised_training, axiom, ! [A] : ((trains(A, summarization_model) & supervised(A)) => supervised_training(summarization_model))).

% The goal: supervised learning is used to train the state-of-the-art text summarization model
fof(goal, conjecture, supervised_training(summarization_model)).