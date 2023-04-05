# Implementační dokumentace k 1. úloze do IPP 2019/2020

jméno a příjmení: Michael Polívka
login: xpoliv07

## 1. Úvod

Zadání bylo implementovat v jazyce PHP 8.1 skript parse.php, který bude provádět lexikální a syntaktickou analýzu jakzyka IPPcode23.

## 2. Implementace

Skript parse.php čte zdrojový kód jazyka IPPcode23 ze standartního vstupu. Výstupem je XML reprezentace programu, která je vypsána na standartní výstup. Chybová hlášení jsou vypisována na standartní chybový výstup.
Skript se skládá z hlavní části, která postupně načítá jednotlivé řádky a kontroluje je pomocí příslušných funkcí. První vždy zkontroluje správnost argumentů a poté vygeneruje XML kód. Pro konstanty probíhá dodatečná kontrola správnosti zápisu opět pomocí regulárních výrazů. Jednotlivé funkce pro generování XML jsou rozděleny podle počtu argumentů. Ke generování XML byla použita knihovna xmlwriter.
