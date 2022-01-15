# Pivot
Pivot is an open source robot similar to Mark Setrakian's [Axis 1 and 2](https://www.youtube.com/watch?v=NsFBHqbNKvA&t=72s).


<img src="https://github.com/neutronztar/RoboClaw/blob/main/media/frontimage.png?raw=true" alt="drawing" width="800" />

## Bill of Materials
### General Parts
| Part                                   | Quantity    | Approx Price   | Total | Notes |
|----------------------------------------|-------------|----------------|------|-------|
| [LX-16A Servo](https://smile.amazon.com/gp/product/B073XY5NT1/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)    | 15          | $20            | $300 | You also need the wires and plastic mounting rings that come with these.
| [JoyStick](https://smile.amazon.com/dp/B08CGYGMJL?psc=1&ref=ppx_yo2_dt_b_product_details) | 1 | $21 | $21 |
| [2 x 0.4 x 8 mm Machine Screws](https://www.boltdepot.com/Metric_socket_cap_Class_12.9_alloy_steel_black_oxide_finish_2mm_x_0.4mm.aspx?Selected=13324) | 400 | $0.0946 | $38 | Exact qty is 300, but you should get some extra. |
| [12V Power Supply](https://www.ebay.com/itm/153588427332) | 1 | $7 | $7 |
| [AC Power Connector](https://smile.amazon.com/dp/B00H8QL53A?psc=1&ref=ppx_yo2_dt_b_product_details) | 1 | $7 | $7 |
| [PETG Filament](https://smile.amazon.com/gp/product/B07PGYHYV8/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1) | 1kg | $23 | $23 |  |
| [Plaster of Paris](https://smile.amazon.com/Dap-Plaster-Paris-20-Min/dp/B008SR3W1G/ref=sr_1_4?crid=1MEP5MWMSY1YV&keywords=plaster+of+paris&qid=1642203001&sprefix=plaster+of+paris%2Caps%2C111&sr=8-4) | 1 | $10 | $10 |  |
| [Round Power Switch](https://www.ebay.com/itm/203485577266?hash=item2f60af8032:g:Sh4AAOSwmDtgvNwT) | 1 | $3 | $3 |  |
| [Power Connector](https://smile.amazon.com/gp/product/B07DCXKNXQ/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1) | 1 | $7 | $7 |  |

### PCB Parts
| Part                                   | Quantity    | Approx Price   | Total | Notes |
|----------------------------------------|-------------|----------------|------|-------|
| [ESP32 DevKit](https://smile.amazon.com/gp/product/B086MLNH7N/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)    | 1           | $7             | $7 |
| [8V Buck Converter](https://smile.amazon.com/dp/B07BDDMGLG?ref=ppx_yo2_dt_b_product_details&th=1) | 1 | $7 | $7 |
| [5V Buck Converter](https://smile.amazon.com/gp/product/B01MQGMOKI/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&th=1) | 1 | $11 | $11 |
| [Molex Spox 3pin Connectors](https://www.mouser.com/ProductDetail/Molex/35301-0340?qs=sGAEpiMZZMskC5GgilGuvsx2BO7CxsBR&countrycode=US&currencycode=USD) | 5 | $0.26 | $1.30 | |
| [1000uF Electrolytic Cap](https://smile.amazon.com/dp/B06XRDWF5X?psc=1&ref=ppx_yo2_dt_b_product_details) | 4 |  | $15 |  |
| [10uF Electrolytic Cap](https://smile.amazon.com/dp/B06XRDWF5X?psc=1&ref=ppx_yo2_dt_b_product_details) | 1 |   |  |  |
| [Tri-State Buffer: SN74LS241N](https://smile.amazon.com/gp/product/B08FZVPJD9/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1) | 1 | $9 | $9 |  |
| Logic Level Shifter SMD: TXS0108EPWR | 1 |   |  | JLC |
| 1k Resistor SMD: 0603WAF1001T5E | 1 |  |  | JLC |
| 10k Resistor SMD: 0603WAF1002T5E | 1 |  |  | JLC |
| 100nF Cap SMD: CC0603KRX7R9BB104 | 2 |  |  | JLC |

### 3D Printed Parts
| Part | Quantity |
|------|------|
| tip.STL | 5 |
| fingerA.STL | 5 |
| knuckle.STL | 5 |
| palm.STL | 1 |
| mid.STL | 1 |
| base.STL | 1 |

#### Approximate Grand Total: $466


## The Code
To make this machine do its magic, every ".py" file in the root of the "MicroPython" directory must be uploaded to the ESP32. I used the utility ["rshell"](https://pypi.org/project/rshell/) to do this. Also the ESP32 must first be loaded with a [MicroPython binary](https://micropython.org/download/esp32/) (tested on v1.17).