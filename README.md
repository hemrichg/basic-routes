# Házi Dolgozat - 12.A, 12.B

## Feladat:
Készítsen egy `Python-Flask` backend applikációt a következőknek megfelelően:

### Endpoint-ok:
- legalább 3db `GET`
- legalább 2db `POST`

### Paraméter használat:
Az alábbiak alkalmazására legyen 1-1db példa mindegyikből:
- path (útvonal) paraméter
- query paraméter
- request body-ba kódolt adat (`html <form>`-al elküldött értékek)
- cookie (süti) szerver oldali küldés és fogadás

### Osztályzás (az alábbiak sorban, egymásra épülnek):
**1** - az applikáció fut
**2** - felvette az endpoint-okat és azok működnek
**3** - tud path és query paramétert feldolgozni
**4** - tud `<form>` adatokat feldolgozni, `cookie`-t küldeni és fogadni
**5** - minden fent leírt pontnak megfelel

### Határidő
***2024. február 19. 23:59***

## Példa projekt:
A példát ezen a linken éri el: [GitHub](https://github.com/hemrichg/basic-routes)
A projekt mappájában 2 fájl található:
- `app.py`
- `test.html`

Az `app.py` tartalmának magyarázata a következő (a `test.html` használatát lásd az ***Applikáció tesztelése*** résznél):


***Hogyan lesz futtatható az app?***

Mindenekelőtt szükséges a `Flask` python modul telepítése. Ezt a következő, terminal-ba írt paranccsal tudjuk megtenni:
```sh
pip install Flask
```
Itt a `pip` parancs a `Python`-hoz tartozó csomagkezelő, a `Flask` maga a csomag.
A projektmappán belül kell egy `.py` kiterjesztésű fájl, ezt fogjuk futtatni (a példában `app.py`). Ahhoz, hogy a webapp fusson, szükséges beimportálni a használt függvényeket, osztályokat. Egy minimális, futó app import része:
```py
from flask import Flask
```
Az app létrehozása és futtatása:
```py
app = Flask(__name__)

if __name__ == "__main__":
  app.run()
```
Egyrészről az `if` sor elhagyható, másrészről a `.run()` függvény, ha megkapja a `debug=True` kapcsolót, nem szükséges nekünk kézzel újraindítani minden alkalommal az appot, ha történt változás a fájlban, mentéskor automatikusan frissül.


***Hogyan veszünk fel endpoint-okat?***

Példa egy `GET` endpoint-ra a `/pelda_get` route-on:
```py
@app.get("/pelda_get")
def get_pelda():
    return "Content for GET"
```
GitHubon az útvonalnál `"/"` szerepel.

Példa egy `POST` endpoint-ra a `pelda_post` route-on:
```py
@app.post("/pelda_post")
def post_pelda():
    return "Content for POST"
```
GitHubon az útvonalnál itt is `"/"` szerepel.


***Hogyan szedünk le path paramétert?***

Példa egy `path_param`-nak elnevezett paraméter használatra:
```py
@app.get("/param/<path_param>")
def get_path_param(path_param):
    return path_param
```
Fontos, hogy a paraméter neve az útvonalban `<` `>` karakterek között szerepeljen. a `get_path_param()`függvény megkapja input-nak a változót, a változó értéke az lesz, amit az `URL`-be írunk a `/param/` után. Ha nem szöveget várunk, a feldolgozáshoz szükséges a megfelelő adattípussá alakítás (nem csak itt, minden használt paraméter esetében).

***Hogyan szedünk le query paramétert?***

Példa egy `q`-nak elnevezett paraméter használatára:
```py
@app.get("/param/query")
def get_query_param():
    return request.args.get("q")
```
A példában szereplő `request` osztály a `Flask` modul része, ezt is szükséges importálni. Az iport sort így kiegészítjük `request`-tel:
```py
from flask import Flask, request
```
Az importált osztályok/függvények vesszővel elválasztva vannak felsorolva.

***Hogyan kezelünk `<form>`-mal küldött adatot?***

Példa egy jelszó küldésre:
```py
@app.post("/param/form")
def get_form_param():
    return request.form["password"]
```

***Hogyan küldünk `cookie`-t szerver oldalról?***

Példa arra, amikor a `token=Session` sütit adjuk a kliensnek:
```py
@app.get("/set_cookie")
def get_scookie():
    response = make_response("Content for cookies")
    response.set_cookie("token", "Session")
    
    return response
```
Ugyanúgy, ahogyan van `request` példány, amiben a request adatait találjuk, deklarálni tudunk a `response`-nak megfelelő párját is. Ehhez a `make_response()` függvényt használjuk, ezt is importáljuk:
```py
from flask import Flask, request, make_response
```
A `make_response()` első argumentuma lesz a visszaküldött tartalom. A sütit új sorban, a `.set_cookie()` fügvénnyel állítjuk, aminek első argumentuma lesz a kulcs, második az érték.

***Hogyan dolgozunk fel klienstől kapott sütit?***

Példa egy `token` kulcsú süti értékének leszedésére:
```py
@app.get("/get_cookie")
def get_gcookie():
    return request.cookies.get("token")
```

### Applikáció tesztelése:
A `Flask` alkalmazásunk alapértelmezetten a `localhost`, `5000`-es portján fut. Tesztelni, hogy elérjük-e a legegyszerűbben a böngésző-be írt `localhost:5000/`-es `URL`-el tudjuk.

***Hogyan tesztelünk `GET` endpoint-ot?***

Beírjük a böngészőbe az adott útvonalat a `localhost:5000/` után. Pl.: `http://localhost:5000/pelda_get`.

***Hogyan tesztelünk `POST` endpoint-ot?***

A példa projektben található egy `test.html` nevű fájl. Ennek tartalma egy eszerű `<form>`, egyetlen gombbal. A `<form>`-nak van két attribútuma:
- `action` - itt adjuk meg, melyik útvonalra szeretnénk request-et küldeni
- `method` - ennek értéke szabja meg, hogy `GET`, vagy `POST` metódust használunk.
Jelen esetben ez `POST`.

A `Flask` appunk alapesetben nem enged hozzáférést a projekt gyökérmappájában található fájlokhoz, így a `localhost:5000/test.html` úton nem érjük el azt. Ehhez a fájl tartalmát ki kell szolgálni valamilyen útvonalon. Példa egy teszt útvonalra, ahol elérjük:
```py
@app.get("/test")
def get_test():
    return send_file("test.html")
```
Fájlok kiszolgálásához a `send_file()` függvényt használjuk, aminek argumentuma lesz a fájl elérési útvonala. Esetünkben ez egy relatív útvonal, a `test.html` fájl rögtön az `app.py` mellett található. A függvényt szintét szükséges importálni:
```py
from flask import Flask, request, make_response, send_file
```
A `<form>` a példában a `localhost:5000/test` úton érhető el. Ha megadtuk az `action`-nek a tesztelendő útvonalat, a gombot megnyomva elküldjük a requestet.

***Hogyan teszteljük az útvonal paramétert?***

A böngészőben beírjuk az adott útvonalat. Ha a példakód szerint tesztelnénk, hogy át tudjuk-e adni az `ezEgyTeszt` szöveges értéket, az `URL` a következő: `localhost:5000/param/ezEgyTeszt`.

***Hogyan tesztelünk query paramétert?***

Hasonlóan az előbbihez, a példa szerinti `URL` eleje a következő: `localhost:5000/param/query`. ehhez jön egy `?` karakter, majd a paraméter neve, és az átadandó érték `=` karakterrel elválasztva.
Pl.: `localhost:5000/param/query?q=ezEgyTeszt`.

***Hogyan tesztelünk `<form>`-mal küldött adatot?***

A `test.html`-en belül, a formot kiegészítjük a kívánt input mezőkkel. A példa szerint a gomb elé rakhatunk mondjuk egy teszt mezőt a `name="password"` attribútummal:
```html
<input type="text" name="password">
```
Ezután a `localhost:5000/test` útvonalon beírunk valami értéket mezőbe és elküldük a korábban is használt gombbal.

***Hogyan teszteljük, hogy sikerült-e a szervernek sütit küldenie?***

A böngészőben `F12`-vel előhozzuk a fejlesztőeszközöket, majd a ***Storage*** menüponton belül a ***Cookies*** fül alatt találjuk a tárolt sütiket. (Az előbbi **Firefox** böngészőnél érvényes, **Chrome** esetében a ***Storage*** az ***Application*** menü alatt található.) Érdemes olyan böngésző profilt használni, ami nincs tele más oldalakhoz tartozó sütikkel (vagy még egyszerűbben egy inkognitó módot nyitni.)

***Hogyan teszteljük, hogy megkaptuk-e a klienstől a sütit?***

Vagy felveszünk a fejlesztőeszközök előbb használt felületén egy új sütit, vagy ha már sikerült küldenünk egyet az appunkból, egyszerűen csak megnyitjuk az adott útvonalat a böngészőből. A példa szerint a két egyszerűbb lépés:
- betöltjük a `localhost:5000/set_cookie` útvonalat
- betöltjük a `localhost:5000/get_cookie` útvonalat

### Kérdés, code review
- `Discord`
- `Email`

A határidőig minden este megnézem, hogy érkezett-e kérdés, kérés. Ha igen, még aznap válaszolok.
