fof(premise1, axiom, ! [X] : (digital_media(X) => ~analog(X))).
fof(premise2, axiom, ! [X] : (printed_text(X) => analog(X))).
fof(premise3, axiom, ! [X] : (streaming_service(X) => digital_media(X))).
fof(premise4, axiom, ! [X] : (hardcover_book(X) => printed_text(X))).
fof(premise5, axiom, streaming_service(obj_1984) => hardcover_book(obj_1984)).
fof(conclusion, conjecture, streaming_service(obj_1984)).