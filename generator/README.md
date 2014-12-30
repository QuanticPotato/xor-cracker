Intro
=====

This tool simply generates a python-like list, containing crypted messages.
These messages are taken from an external file (This way, it's easy to modify
it).

Building and running
====================

To build the tool, you just need a working C compiler, and a make-like program.
Then, run :
	make

The tool output the generation on the standard output, so you should use UNIX
pipes to write it in a file :
	./generator quotes > messages.py

Quotations
==========

The quotations available in the quotes file just stand as an example.
I grabbed them on http://www.brainyquote.com/.
You can of course use different messages.
