# Minecraft Console Reader Docs

# Project Setup

Der Modul Ordner muss sich im Projekt Ordner befinden.

Neben dem eigentlichen Python Programm muss der Titel des Konsolen-Fensters angepasst werden, dazu fügt man folgende Zeile in die Start Datei des Servers ein:

```
title `NEWNAME`
```

WICHTIG: Dieser Name muss später auch im Programm übernommen werden!

Um den `ConsoleReader` zu initialisieren benötigt man das entsprechende Modul.

```python
from Module.consolecontroller import ConsoleController, ResponseTypes

cc = ConsoleController(log_path, `NEWNAME`)
rec, log, console = cc.get_util()
```

Durch die letzte Zeile erhält man die einzelnen Teile der Klasse. (Receiver, Log, Konsole)

Als nächstes wird eine Schleife benötigt.

Die `cc.delay()` Funktion hat als default einen Delay von 0.1 Sekunden. Die Zeit kann als Parameter verändert werden.

```python
while True:
		update()
		cc.delay()
```

Die Update Funktion muss extra erstellt werden.

In dieser können weitere Interaktionen mit dem Modul statt finden.

Basisprojekt:

```python
from Module.consolecontroller import ConsoleController, ResponseTypes

cc = ConsoleController(log_path, NEWNAME)
rec, log, console = cc.get_util()

def update():
	pass

while True:
		update()
		cc.delay()

```

# Funktionen

## Console:

```python
console.sendToConsole(`MESSAGE`)
```

Dieser Befehl führt die mitgegebene `MESSAGE` in der Konsole aus.

```python
console.tellraw(`Tellraw Object`)
```

Dieser Befehl schickt einen Tellraw-Befehl an die Konsole.

```python
console.create_tellraw_from_dict(`player`,`txt`)
```

`Player`: Ein Minecraft Selector (`@A, @e,` usw.) Oder ein `Spielername`

`Txt`: Ein JSON Tellraw-Befehl wie man ihn in Minecraft schreiben würde (`Dictionary`)

# Receiver:

```python
receiver.is_resp(`ResponseType`)
```

Gibt `True` zurück, wenn der Type des Respond-Objects == dem Param

```python
receiver.is_msg(`msg`)
```

Gibt `True` zurück wenn `msg` der Nachricht der Response entspricht.

```python
receiver.is_cmd(`PREFIX`)
```

Gibt `True` zurück wenn die Nachricht der Response das `PREFIX` an erster Stelle hat.

```python
receiver.get_cmd()
```

Gibt ein `Command Object` zurück.

```python
receiver.is_scoreboard(`board`)
```

Gibt `True` zurück, wenn `board` dem Response Scoreboard entspricht.

```python
receiver.trigger_reset_value()
```

Sendet den Befehl um das Scoreboard des Spielers, der den Trigger Befehl ausgeführt hat zurück zu setzten.

```python
receiver.get_res(y=None)
```

Gibt das Response-Dictionary zurück. Wenn `y` == String ist der Rückgabewert Response[`y`]

# Response Object:

```python
Response(`typ,extra`)
```

`Typ` : ResponseType

`Extra`: Dictionary mit beliebigen Keys und Values

`Self.response`: Typ und Extra zusammengefügt

# Log:

```python
log.get_changes()
```

Bei Veränderungen in der Log Datei gibt diese Funktion die Veränderung zurück. Sonst gibt sie `None` zurück.

```python
log.format_return()
```

Gibt das `Response Object` des letzten Log-Eintrags zurück.

Bei einem `execute if` Befehl wird `True` oder `False` zurück gegeben.

Sollte der Eintrag nicht zu geordnet werden können, wird ein `Response Object` mit dem `Type`: TEXT, `txt`: letzter Eintrag zurück gegeben.

# Console Controller:

```python
cc.check_for_message()
```

Gibt `True` zurück, wenn der letzte Log-Eintrag eine `Message` von einem Spieler ist.

```python
cc.check_for_updates()
```

Gibt `True` zurück, wenn sich der letzte Log-Eintrag verändert (siehe Log.get_changes())

```python
cc.run_cmds(`PREFIX`)
```

Führt alle Registrierten Commands aus.

```python
cc.get_util()
```

Gibt den `Receiver`, das `Log`und die `Console` zurück.

# DataBase:

```python
db = DataBase(`FILEPATH`)
```

`FILEPATH`: Pfad zur JSON-Datenbank

```python
db.read()
```

Updated die `[self.data](http://self.data)` Variable auf die aktuellen Daten aus der Datenbank.

```python
db.write()
```

Schreibt die Variable `[Self.data](http://Self.data)` in die Datenbank Datei.

# Command Registrieren

Um einen eigenen`Command`zuerstellen  muss zunächst eine extra Datei erstellt werden. 

In der Datei können mehrere `Klassen` erstellt werden, welche die Klasse `ParentCommand` als Erbe hat.

```python
from Module.command import ParentCommand

class NewCommand(ParentCommand):
			def __init__(self,receiver, console):
```

Der ParentCommand muss in der **init** Funktion initialisiert werden und benötigt die Parameter `Receiver,Console`

Um die Funktionalität des Commands zu erstellen wird eine Funktion `execute(self)` benötigt, diese wird ausgeführt sobald der Spieler den passenden Befehl in den Chat schreibt. Die Funktion muss am Ende der **init** Funktion aufgerufen werden.

Sobald du zufrieden mit deinem Command bist musst du ihn noch `Registrieren`

```python
COMMANDS = [
	{"name":`COMMANDNAME`}
]
```

In dieses Dictionary musst du jeden Befehl eintragen mit dem Namen der Klasse.

In deiner Main-Datei musst du die Commands jetzt noch an den `ConsoleController` weiter geben:

```python
from `COMMANDDATEI` import COMMANDS

...
cc.commands = COMMANDS
```

Basic-Command:

```python
from Module.command import ParentCommand

class NewCommand(ParentCommand):
		def __init__(self,receiver,console):
				ParentCommand.__init__(self, receiver, console)
		

				self.execute()

		def execute(self):

			# Aktionen

```

# Response Types

Import:

```python
from Module.consolecontroller import ResponseTypes
```

Alternativ sind die RespondTypes auch im Log-Object vorhanden:

```python
log.RespondTypes
```

`DATA`: data get entity

```python
{"type":DATA,"player":player, "data":Return von /data command}
```

`DATA_BLOCK`: data get block

```python
{"type":DATA_BLOCK,"block":block_pos, "data":Return von /data command}	
```

`PLAYER_MSG`: Player Message im Chat

```python
{"type":PLAYER_MSG,"player":player, "msg":gesendete Nachricht}
```

`TEXT`: nicht zugeordnete Response

```python
{"type":TEXT,"Txt":Log-Nachricht}
```

`TRIGGER`: Trigger Befehl

```python
{"type":TRIGGER,"player":player,"scoreboard":scoreboard,"value":value}
```

`SCOREBOARD_SET`: Scoreboard Players set

```python
{"type":SCOREBOARD_SET,"player":player,"scoreboard":scoreboard,"value"}
```

# Tellraws

Um einen Tellraw Befehl zu generieren kannst du die Funktion `console.tellraw()` verwenden welche ein Tellraw-Object als Parameter nimmt.

## Tellraw-Object:

Parameter:

`Player`: der Spieler an den die Nachricht geschickt werden soll

`Parts`: eine Liste von Part-Objekten

## Part-Object:

Parameter:

`Txt`: Der Text in diesem Teil des Tellraw-Befehls [BOOL]

`Color`: Farbe des Textes [BOOL]

`Bold`: Dickgedruckt [BOOL]

`Italic`: kursiv [BOOL]

`Underlined`: unterstrichen [BOOL]

`Strikethrough`: Durchgestrichen [BOOL]

`Obfuscated`: Unleserlich [BOOL]

Wenn sich in deiner Tellraw-Nachricht einer dieser Parameter verändert sollen, brauchst du mehrere Parts, welche die angepassten Parameter beinhalten.