# Dinamiskās darba telpas aizpildīšana

### Formulējums

Doti `n` darbinieki, kur katram no viņiem saraksts ar laika intervāliem (dienām) `vacation[i][]`, kad tie nav pieejami, 
kā arī kopējā slodze (viens var strādāt pilnu, cits pusslodzi). 

Darbinieki ir sadalīti `m` struktūrvienībās (katrs darbinieks tieši vienā struktūrvienībā).

Dotas `k` darba vietas un `t` darba dienas - kopā `2*k*t` laika logi, 
kad ir iespējams darbs klātienē (pieņem, ka katrai darba vietai ir `2` šādi logi katrā darba dienā). 

Izvietot darbiniekus laika logos tā, ka darbinieks nav nodarbināts laikā, kad viņš nav pieejams, 
viņa darba laiks nepārsniedz viņa slodzi, kā arī katras struktūrvienības darbinieki pavada vismaz `1/3` laika klātienē!

### Mainīgie un konstantie

#### Mainīgo uzskaitījums un atšifrējumi
* `N` - darbinieku skaits, pozitīvs skaitlis;
* `M` - struktūrvienību skaits, pozitīvs skaitlis;
* `K` - darba telpā esošās darba vietas, pozitīvs skaitlis;
* `T` - darba dienu skaits, pozitīvs skatlis;
* `VACATION` - darbinieku atvaļinājums, piesaistīts konkrētam darbiniekam

#### Konstanti skaitļi
* `2` - pieejamie laika logi dienā katrai darba vietai telpā;
* `1/3*T` - minimālais laiks, kas struktūrvienībai jāpavada klātienē.