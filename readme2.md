Implementační dokumentace k 2. úloze do IPP 2022/2023 
Jméno a příjmení: Michael Polívka 
Login: xpoliv07

## 1. Úvod

Zadání bylo implementovat v jazyce Python 3.10 skript parse.php, který bude načte XML reprezentaci programu v IPPcode23 a následně interpretuje obsah a generuje výstup.

## 2. Implementace

### 2.1 Spuštění
Skript interpret čte vstup buď ze souboru nebo ze standarního vstupu. Výstupem je pak interpretace programu samotného a jeho případné vypsání.  
Vše je zaobaleno do třídy Interpret, kde se pro instanciaci vytváří jedináčci _Frame_ a _Flow\_Manager_, kteří se společně starají o zachování kontextu programu. 
_Flow\_Manager_ v sobě uchovává informace o běhu programu (pořadí právě prováděné instrukce, seznam návěští, zásobník volání) a _Frame_ je instancí zásobíku rámců, uchovává v sobě veškerou logiku pro správnou práci s proměnnými.  
Následně proběhne zpracování a kontrola argumentů příkazové řádku pomocí knihovny _argparse_, proběhne nastavení argumentů _source_ a _input_, buď na příslušný soubor nebo _stdin_
### 2.2 Rozbor XML
Třída _XML\_parse_ se stará o syntaktickou kontrolu XML dokumentu a následně o vytvoření seznamu jednotlivých instrukcí a k nim příslušným argumentům. Pro rozbor XML je použita knihovna _xml.etree.ElementTree_.

### 2.3 Tvorba seznamu instrukcí
Každá jednotlivá instrukce jazyka IPPCode23 má svoji vlastní třídu která je potomkem třídy _Instruction_, která implementuje pomocné metody pro získávání dat a kontrolu argumentů pro jednotlivé potomky. Jednotlivé typy operandů (Var, Const, Type, Label) mají každý svou vlastní třídu, pro jednodušší práci s daty a identifikaci.

### 2.4 Interpretace 
Po vygenerování seznamu instrukcí, se provede první průchod při kterém se vygenerují všechna návěští v programu a uloží se do _Flow_Manager_, současně se zkontroluje duplicita návěští a instrukce _LABEL_ se nahradí pomocnou instrukcí _LABEL\_SUBSTITUTE_, která slouží pouze jako zástupce.
Při druhém průchodu se pro jednotlivé instrukce volá metoda _Instruction.exec()_ která v sobě obsahuje kód pro její správné provedení. Druhý průchod probíhá tak dlouho dokud se nenarazí na inkrukci _EXIT_ nebo na konec seznamu reprezentovaný jako _None_.

### 2.5 Testování
Pro testování byly použity primárně tyto [testy](https://github.com/Nevoral-Leos/IPP_interpret-only_test_2023).
### 2.6 UML diagram
![UML Diagram](./classes.png)