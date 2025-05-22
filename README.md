# IKS pārlidojumu plānotājs

## Projekta uzdevums
Šis python skripts terminālī izvada informāciju par redzamiem Internacionālās kosmosa stacijas pārlidojumiem pāri konkrētai pozīcijai (izteiktai ģeogrāfiskās koordinatēs platuma un garuma grādos) tuvāko 10 dienu laikā, kā arī gaidāmos laikapstākļus atrastajos laikos.

Kods izmanto API piekļuves un tīmekļa lapu skrāpēšanu datu iegūšanai:
 - Pārlidojumu datu iegūšanai tiek skrāpēta lapa [Heavens-Above](https://heavens-above.com/), izvēlēts, jo ir viens no retajiem IKS pārlidojumu datu resursiem, kurus atļauts skrāpēt
 - Ierīces pozīcijas iegūšanai tiek izsaukts API [ip-api](ip-api.com), izvēlēts tā vienkāršības dēļ
 - Laikapstākļu datu iegūšanai tiek izsakuts API api.open-meteo.com, izvēlēts tā pilvērtīgo datu un bez atslēgas iespējamās izmantošanas dēļ


## Prasības / izmantotās bibliotēkas

- Python 3.x  
- requests  
- beautifulsoup4
- datetime
- re

Instalēt prasības, kas nav iekļautas standarta pyhton instalācijā var izmantojot termināli, ar pip:  
```bash
pip install requests beautifulsoup4
```
- "Requests" lietots tīmekļa lapas "Heavens-Above.com" un API piekļuvei
- "Beautifulsoup4" lietots skrāpēto lapu HTML apstrādei par lietojamiem datiem.
- "datetime" lietots laika, datumu un laika zonu apstrādei un lieotšanai
- "re" lietots lai ar REGEX palīdzību apstrādātu lietotāja ievadītos datus (koordinātas)

## Metodes
### metode  get_iss_passes
```python
get_iss_passes(lat, long)
```
Metode pieņem koordinātas (platuma un garuma grādos) 
metode atgriež vārdnīcu ar tuvāko 10 dienu IKS pārlidojumiem un to datiem doto koordinātu vietā.
### metode get_weather_condition
```python
get_weather_condition(lat, lon, dt)
```
Metode pieņiem koordinātas (platuma un garuma grādos) un datetime objektu 
Metode atgriež laikapstākļu aprakstu (vienā vārdā) doto koordinātu vietā, dotajā laikā
### metode get_coordinates
```python
get_coordinates()
```
Metode mainīgos nepieņem
Metode lietotājam pieprasa ievadīt koordinātas (platuma un garuma grādos), kā arī pārbauda vai ievade ir pareiza.

## Lietošana / darbība

1. Programma vispirms prasa vai vēlaties ievadīt koordinātas:
- Ja atbildēts "n", programma lieto iekārtas koordinātas, kas iegūtas no IP adreses
- Ja atbildēts "y", programma pieprasa ievadīt platuma un tad garuma grādus decimālā formātā

2. Programma tad pārmeklē lapu heavens-above.com ņemot vērā dotos datus un lejuplādē tabulu ar IKS pārlidojumu datiem.
3. Programma katram pārlidojumam piemeklē tā norisošajā laikā prognozētos laikapstākļus
4. Programma izvada atrastos datus

## To-Do
- [ ] Ieviest kļūdu apstrādi nesasniedzmu lapu vai API kļudu gadījumā
