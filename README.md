#python library to get staying time and your activity data easily from Moves API

## Example Usage

```
from moves import Place,Summary

p = Place("20141027")
print p.getPlaceSec("home")
# 57373.0

s = Summary("20141027")
print s.getActivitySec("running")
# 135.0
print s.getActivityMeter("running")
# 324.0

```

At first, you should authorize yourself and register your place on PLACEINFO.tsv

## Authorization

```
from moves
m.authorization()
```

Access the URL, input PIN code and then get code from redirect URL.
then, you put code into moves.py.

```
def authorization():
    ---
    tempCode = u" WRITE CODE YOU HAVE GOT"
    ---
```

```
import moves
moves.authorization()
```

Now you again execute authorization() func, you get access_token and write it on USERINFO

```USERINFO.tsv
<<< client_id >>>
<<< client_secret >>>
<<< redirect_url >>>
<<< oauth_url >>>
<<< api_base_url >>>
<<< access_token >>>
```


## register your places on PLACEINFO.tsv
you need to your "home" or "office" placeID on PLACEINFO

you can confirm placeID in this way

```
from moves import Moves
from pprint import PrettyPrinter as pp

m = Moves()
p = pp()
p.print(m.get_places("20141027"))
```

and then, you should put place ids on PLACEINFO.tsv in way below

```PLACEINFO.tsv
home	482937349
lab	453829
lab	482945
office	482973243
office	409287349
```