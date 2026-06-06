% Positive run: prove streaming_service(year_1984)
fof(ax1, axiom, ! [X] : (digital_media(X) => ~analog_media(X))).
fof(ax2, axiom, ! [X] : (printed_text(X) => analog_media(X))).
fof(ax3, axiom, ! [X] : (streaming_service(X) => digital_media(X))).
fof(ax4, axiom, ! [X] : (hardcover_book(X) => printed_text(X))).
fof(ax5, axiom, streaming_service(year_1984) => hardcover_book(year_1984)).
fof(goal, conjecture, streaming_service(year_1984)).