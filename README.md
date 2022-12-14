# Ratageneraattori

Ohjelman tarkoituksena on generoida valokuvasta rata piirrustusohjelmalle ja se sisältää mahdollisuuden parametrien syöttämiseen kuvankäsittelyalgoritmille sekä filtterille.  Ohjelma on jaettu kolmeen osaan: malliin, näkymään ja kontrolleriin. Malli sisältää säilyttää ohjelman sisältämän datan ja muokkaa sitä. Näkymä sisältää käyttöliittymän komponentit. Kontrolleri ohjaa mallin ja näkymän toimintaa käyttäjän toiminnan perusteella. 

 Rata tallenetaan JSON tiedostona jotta sitä voi soveltaa myös web-sovellukseen:
 ```json
[
 {
  "x": 1,
  "y": 1,
  "z": 1
 },
 {
  "x": 2,
  "y": 2,
  "z": 2
 },
 {
  "x": 3,
  "y": 3,
  "z": 3
 },
 ...jne
```

 

 

Projektista voi luoda .exe tiedoston pyinstallerilla seuraavalla komennolla:
```
pyinstaller --onefile controller.py
```
.exe tiedoston kanssa samaan tiedostoon on lisättävä repositysta löytyvä 'valkoinen.png'

## Työssä käytetyt kirjastot

1. Tkinter
2. OpenCv
3. Numpy
4. Scipy
5. Math
6. json
7. (Firebase)



## GIF
<img src="https://github.com/svhein/gif/blob/main/lentsikka2.gif" height="600" width="800" />
