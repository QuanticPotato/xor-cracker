xor-cracker  (French README, english below)
===========================================

Ce projet existe simplement dans le but de resoudre un probleme cryptographique :

- Retrouver la cle XOR qui a encrypte plusieurs messages (comme par exemple des citations) composees de caracteres imprimables.

La difficulte repose sur le fait que l'on ne dispose que des messages cryptes.

Architecture du projet
----------------------

Arboressence et role des differents dossiers qui composent le projet :

generator/
	Contient un outil qui permet de crypter une citation a l'aide d'une cle generee aleatoirement.
	Le message crypte est ensuite transmit sous forme de fichier source, directement exploitable dans le reste du projet.

c/
	Contient la version C de xor-cracker

python/
	Contient la version python de xor-cracker



xor-cracker (English README)
============================
