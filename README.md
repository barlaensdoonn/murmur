# murmur

## dependencies
#### *gpiozero*
```
sudo apt-get update
sudo apt-get install python3-gpiozero
```

#### *relay repo nested inside this repository*
[link to the repo](https://github.com/barlaensdoonn/relay)
```
cd ~/gitbucket/murmur
git clone https://github.com/barlaensdoonn/relay.git
```

## connections
#### *sainsmart 5V 4-channel relay board*
[link to the board](https://www.sainsmart.com/products/4-channel-5v-relay-module?nosto=customers-also-bought)
```
raspi connections to relay board:
    3.3V -> VCC
    5V -> JD-VCC
    GND -> GND
    GPIO -> IN*

power supply connections to relay terminals:
    +V power supply -> +V power input
    GND power supply -> NO relay terminal (far left when facing the relay terminals) -> GND power input
```
