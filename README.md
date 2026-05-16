# ccg-proxy-maker

## Usage
There are a couple of ways to use. The best way is to use the comb feature which allows both JP and ENG cards to be generated to a single PDF with modular control over each card's translation

```
Example
JP,GIM/W124-037EX,4,,,,,,NT

<LANG>,<CARD>,<QUANTITY>,<empty space>,<ANCHOR-TOP>,<ANCHOR-LEFT>,<ANCHOR-RIGHT>,<ANCHOR-BOTTOM>,<TRANSLATE>
```

```
<LANG> := JP | EN
<CARD> := <SERIES>/<SET>-<CARD_ID>
<QUANTITY> := <number>
<empty space> := anything (this is not used)
<ANCHOR-TOP> := <number>
<ANCHOR-RIGHT> := <number>
<ANCHOR-LEFT> := <number>
<ANCHOR-BOTTOM> := <number>
<TRANSLATE> := T | NT (by default with translation setting on in main all cards will be translated if Japanese)
```
### Using anchor
You need 3 positive value (pixels on image) and 1 negative value (-1) for the text box to grow to accomodate the size of the overall generated text. By default there is a setup for anchors for all cards. This is really used so far when card text are in a nonstandard on the card.

For example, for the below setup, the top anchor is unbound meaning the box will grow upwards. 
```
<ANCHOR-TOP> := -1
<ANCHOR-RIGHT> := 3
<ANCHOR-LEFT> := 3
<ANCHOR-BOTTOM> := 3
```
### Document DIM
By default the document dims are located in ```model/document.py```. This is where you manipulate the output of the document at 300 DPI. Output doc will be scaled up or down to the default document dims. Due to the nature of printing in printable area, smaller document dims will result in larger output in cards in general vice versa. Use this to fine tune card sizes from prints.
### ENG Sources
Images for english actually have weird image url which you can add the pattern manually in ```LOCAL_DB``` inside of main. Better solutions will be introduced later.
### JP Sources
JP sources will use the CCondeluci db by default but can be manually added. Look at the ```jpdb``` directory for examples. You can also add to ```jp_base``` in ```card_db.py```. The order of override for same card id is ```jp_base``` > ```jpdb``` > CCondeluci db
### Translation
Get a Japanese Chinese font like the one below or install directly to system. Change the font file path in ```util/text.py```
```
https://github.com/notofonts/noto-cjk/blob/main/Sans/OTC/NotoSansCJK-Light.ttc
```
### Errors
If errors exist due to image fetch issues it is probably due to mismatch of id. Check the card against the official ws tcg website foir the actual image URL. For example, ```OVL/S99-E076SP``` is actually ```OVL/S99-E076R``` in the image url, so therefore you will use the second one as the card in deck list