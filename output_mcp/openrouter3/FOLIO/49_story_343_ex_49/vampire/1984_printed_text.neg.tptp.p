% Problem: 1984 is printed text - Negative version
fof(no_digital_analog, axiom, ! [X] : (digital_media(X) => ~analog_media(X))).
fof(printed_is_analog, axiom, ! [X] : (printed_text(X) => analog_media(X))).
fof(streaming_is_digital, axiom, ! [X] : (streaming_service(X) => digital_media(X))).
fof(hardcover_is_printed, axiom, ! [X] : (hardcover_book(X) => printed_text(X))).
fof(streaming_1984_implies_hardcover, axiom, streaming_service(book_1984) => hardcover_book(book_1984)).
fof(goal, conjecture, ~printed_text(book_1984)).