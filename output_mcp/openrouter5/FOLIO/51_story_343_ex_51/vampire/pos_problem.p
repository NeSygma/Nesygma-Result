% Positive version: original conclusion as conjecture
% Conclusion: 1984 is not a streaming service.
fof(premise_1, axiom, ! [X] : (digital_media(X) => ~analog(X))).
fof(premise_2, axiom, ! [X] : (printed_text(X) => analog_media(X))).
fof(premise_3, axiom, ! [X] : (streaming_service(X) => digital_media(X))).
fof(premise_4, axiom, ! [X] : (hardcover_book(X) => printed_text(X))).
fof(premise_5, axiom, (streaming_service(c_1984) => hardcover_book(c_1984))).

fof(goal, conjecture, ~streaming_service(c_1984)).