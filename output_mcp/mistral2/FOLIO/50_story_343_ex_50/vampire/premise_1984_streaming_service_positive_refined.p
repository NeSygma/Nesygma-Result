fof(digital_media_def, axiom, ! [X] : (digital_media(X) => ~analog_media(X))).
fof(printed_text_def, axiom, ! [X] : (printed_text(X) => analog_media(X))).
fof(streaming_service_def, axiom, ! [X] : (streaming_service(X) => digital_media(X))).
fof(hardcover_book_def, axiom, ! [X] : (hardcover_book(X) => printed_text(X))).
fof(conditional_premise, axiom, (streaming_service(n1984) => hardcover_book(n1984))).
fof(constant_1984, axiom, n1984 = n1984).
fof(goal, conjecture, streaming_service(n1984)).