fof(premise1, axiom, ! [X] : (digital_media(X) => ~analog_media(X))).
fof(premise2, axiom, ! [X] : (printed_text(X) => analog_media(X))).
fof(premise3, axiom, ! [X] : (streaming_service(X) => digital_media(X))).
fof(premise4, axiom, ! [X] : (hardcover_book(X) => printed_text(X))).
fof(premise5, axiom, streaming_service(c1984) => hardcover_book(c1984)).
fof(goal, conjecture, streaming_service(c1984)).