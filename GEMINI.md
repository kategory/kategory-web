In allen Dateien mit Einrückung, rücken wir immer 3 Spaces, keine TAB, ein.

Wir nutzen Bootstrap 5, Es soll so verwendet werden, dass "Responsive Design" optimal unterstützt wird.

Es handelt sich hier um eine WebSeite, die auf GitHub gehostet werden können muss.

Grundlegende css Einstellungen sollen in kategory.css im root abgelegt werden.

kategory ist light-mode.

Es gibt ein Logo in der Datei kategory.svg. Das soll auf beiden sites eingebunden werden.

Die Schritarten sind:
- font-family: "Times New Roman", Times, Baskerville, Georgia, serif;
- Für Mono-Space nutzen wir den Font-Stack: font-family: 'Consolas', 'Monaco', 'Menlo', 'Ubuntu Mono', 'source-code-pro', monospace;

Es folgen die Farben in RGB. Sie sind im Dark - und Light-Mode in gleicher weise zu verwenden.

Dunkelgrau: 87/86/86
Rot       : 227/6/19

Grün      : 0/234/0
Gelb      : 252/228/0
Orange    : 255/126/0
Hellblau  : 0/240/240
Dunkelblau: 25/118/225

Weiß      : 255/255/255
Schwarz   : 0/0/0

Die normalen Farben für Text und so sind Schwarz und Weiß.

Rot nutzen wir für sehr wichtige Akzente
Dunkelgrau für geometrische gestalltungen (Rahmen, dunkle Flächen ... )

kategory wird spätetr über kategory.de erreicht werden

## Menü-Integration
Das Navigationsmenü der Webseite wird nach dem "Client-Side Include"-Prinzip per JavaScript geladen (Single Source of Truth), damit Änderungen am Menü nur an einer zentralen Stelle erfolgen müssen:
- **`menu.html`**: Enthält ausschließlich die HTML-Struktur des Bootstrap-Menüs. Alle Links innerhalb der `menu.html` müssen **absolut** adressiert werden (z. B. `href="/index.html#prozesse"` statt relativer Pfade), da das Menü aus unterschiedlichen Verzeichnistiefen (z. B. aus dem `/blog`-Ordner) geladen wird.
- **`menu.js`**: Ein kurzes Skript, das die `menu.html` per `fetch("/menu.html")` (ebenfalls absolut adressiert) lädt und in den DOM einfügt.
- **Einbindung in Seiten**: Jede HTML-Seite, die das Menü anzeigen soll, benötigt an der gewünschten Stelle den Platzhalter `<div id="menu-container"></div>` und muss vor dem schließenden `</body>`-Tag das Skript `<script src="/menu.js"></script>` einbinden.
- **Lokales Testen**: Aufgrund der CORS/Same-Origin-Policy von Browsern kann das lokale Testen dieses Setups nicht über das `file:///`-Protokoll erfolgen. Es muss ein lokaler Webserver gestartet werden (z. B. `python -m http.server 8000` im Root-Verzeichnis), um die Seite unter `http://localhost:8000` aufzurufen.

## Umgang mit Skripten (Agenten-Policy)
Im Zuge der Entwicklung mit KI-Agenten fallen häufig kleine Migrations- oder Automatisierungsskripte an (z. B. Skripte, die einmalig Text in vielen Dateien ersetzen). Da der Aufwand zur Erstellung solcher Skripte minimal ist, gilt folgende Regelung:
- **Einmal-Skripte** (z. B. temporäre Migrationen) werden **nicht** in das Versionskontrollsystem (Git) übernommen. Sie sind nach erfolgreicher Ausführung sofort wieder zu löschen, um technische Schulden und "toten Code" im Repository zu vermeiden.
- **Wiederkehrende Werkzeuge**, die regelmäßig im Betrieb oder Build-Prozess benötigt werden, gehören hingegen ins Repository (idealerweise in einen separaten `/scripts`- oder `/tools`-Ordner).
