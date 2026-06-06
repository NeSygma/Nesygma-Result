fof(premise_1, axiom, ! [X] : (digital_media(X) => ~analog_media(X))).
fof(premise_2, axiom, ! [X] : (printed_text(X) => analog_media(X))).
fof(premise_3, axiom, ! [X] : (streaming_service(X) => digital_media(X))).
fof(premise_4, axiom, ! [X] : (hardcover_book(X) => printed_text(X))).
fof(premise_5, axiom, (streaming_service(1984) => hardcover_book(1984))).
fof(goal, conjecture, streaming_service(1984)).