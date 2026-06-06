% Negative test: Is the negation of "1984 is printed text" entailed?
fof(premise1, axiom, ! [X] : (digital_media(X) => ~analog_media(X))).
fof(premise2, axiom, ! [X] : (printed_text(X) => analog_media(X))).
fof(premise3, axiom, ! [X] : (streaming_service(X) => digital_media(X))).
fof(premise4, axiom, ! [X] : (hardcover_book(X) => printed_text(X))).
fof(premise5, axiom, (streaming_service(x1984) => hardcover_book(x1984))).
fof(goal_negated, conjecture, ~printed_text(x1984)).