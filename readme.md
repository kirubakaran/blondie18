The name blondie18 was inspired by [this project](http://en.wikipedia.org/wiki/Blondie24).

Evolve blondie by running genblondie.py. You can set the parameters in
a section in blondie.conf

```
 % ./genblondie.py --help
usage: genblondie.py [-h] [--loadfromdisk] --configsection CONFIGSECTION

Create Connect-4 AI Players

optional arguments:
  -h, --help            show this help message and exit
  --loadfromdisk
  --configsection CONFIGSECTION
                        Name of the config section in ./config to use. You can
                        say: default
```

---

You can play with blondie like this:
```
./blondie18.py --blondiebrain latest --datadir /media/tera/blondiehome --printit
```
Or
```
./blondie18.py --blondiebrain blondie-bestof-gen00000.xml --datadir /media/tera/blondiehome
```

```
 % ./blondie18.py --help 
usage: blondie18.py [-h] [--printit] [--debug] [--moves MOVES]
                    [--autopilot AUTOPILOT] --datadir DATADIR --blondiebrain
                    BLONDIEBRAIN

Play Connect-4

optional arguments:
  -h, --help            show this help message and exit
  --printit
  --debug
  --moves MOVES
  --autopilot AUTOPILOT
  --datadir DATADIR
  --blondiebrain BLONDIEBRAIN
                        Provide file name of the blondie neural network to
                        load. Enter "latest" to load the latest.
```
