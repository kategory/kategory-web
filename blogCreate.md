**Aufgabenstellung:**  
Erstelle aus der Markdown-Datei *blog.md* statisches HTML.

**Struktur:**

1. **Übersichtsseite:** Eine Hauptseite, die alle Blogeinträge auflistet. Sie heißt blog.html  
2. **Unterverzeichnis:** Ein Verzeichnis namens *blog/*.  
3. **Detailseiten:** In diesem Unterverzeichnis soll für jeden Blogeintrag eine HTML-Unterseite erstellt werden.

**Formatierungsregeln:**

* **Grunddesign:** Verwende für die Übersichtsseite und die Detailseiten das Framework Bootstrap, orientiert an der Struktur der Datei *logismy.html*
 (Indexseite des Schwesterprojekts, aber wir verwenden hier nicht die logismy.css und wir haben lightmode).  
* **Blogeinträge (Markdown):** Jeder Blogeintrag beginnt mit einer Hauptüberschrift (eine Raute *\#*).  
  * Die vorangestellte Nummerierung (z. B. "6.5") ist zu ignorieren.  
  * Die Überschrift dient als Titel (auf der Übersichtsseite und der Detailseite).  
* **Dateinamen:** Erzeuge aus der Überschrift den Dateinamen für die jeweilige HTML-Seite:  
  * Verwende Minuszeichen zur Worttrennung.  
  * Nutze ausschließlich 7-Bit-ASCII-Zeichen.  
  * Der Name muss (bei Ersatz der Minuszeichen durch Unterstriche) einem gültigen Python-Variablennamen entsprechen.  
  * Maximale Länge: 32 Zeichen.  
* **Metadaten:**  
  * Autor: Ignorieren.  
  * Datum: Konvertiere das Format "Tag. Monatsname" (z. B. "12. März") in das Zielformat "TT. MMMM YYYY" (z. B. "12. März 2026").  
  * Lesezeit: Ignorieren.  
  * Das Datum soll im Dateinamen der Einzeldatei links als YYYY-MM-TT- stehen, sodass wir nach datum sortieren können.
* **Inhalt & Layout:**  
  * Übernehme die Markdown-Formatierungen (Überschriften mit zwei Rauten *\#\#* usw.) als HTML-Elemente.  
  * **Übersichtsseite:** Zeige pro Blogeintrag nur den Textabsatz bis zur ersten Unterüberschrift (Ebene *\#\#*).  
  * **Kategorien:** Die am Ende der Einträge aufgeführten Links (Kategorien in eckigen Klammern inkl. URL) sind vollständig zu ignorieren.  
  * **Reihenfolge:** Die Blogeinträge sollen chronologisch absteigend (jüngste zuerst) sortiert sein. Das ist auch die jetzige Reihenfolge in  *blog.md*