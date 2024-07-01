
<p align="center">
    <a href="https://pypi.python.org">
        <img src="https://ben-nour.com/images/geojson-shave.png" alt="GeoJSON-shave" style="width: 60%; height: auto;"/>
    </a>
</p>

<p align="center">
     <a href="https://github.com/ben-n93/geojson-shave/actions/workflows/tests.yml"><img src="https://github.com/ben-n93/geojson-shave/actions/workflows/tests.yml/badge.svg"                 alt="Testing"></a>
     <a href="https://github.com/ben-n93/geojson-shave/blob/main/LICENSE"><img src="https://img.shields.io/pypi/l/geojson-shave" alt="License"></a>
    <a href="https://codecov.io/gh/ben-n93/geojson-shave" ><img src="https://codecov.io/gh/ben-n93/geojson-shave/graph/badge.svg?token=XUMK0D4J9X"/></a>
    <a href="https://pypi.org/project/geojson-shave/"><img src="https://img.shields.io/pypi/pyversions/geojson-shave" alt="versions"></a>
    <a href="https://github.com/tmcw/awesome-geojson"><img src="https://awesome.re/mentioned-badge.svg" alt="awesome list badge"></a>
</p>

---

geojson-shave reduces the size of GeoJSON files by:

- Reducing the precision of latitude/longitude coordinates to the specified decimal places.
- Eliminating unnecessary whitespace.
- (Optionally) replacing the properties key's value with null/empty dictionary.

This tool assumes that your GeoJSON file conforms to the [RFC 7946](https://datatracker.ietf.org/doc/html/rfc7946).

Please be aware that when you use fewer decimal places you can lose some accuracy. _"The fifth decimal place is worth up to 1.1 m: it distinguish trees from each other"_ - read more [here](https://gis.stackexchange.com/questions/8650/measuring-accuracy-of-latitude-and-longitude).

## Installation
```
$ pip install geojson-shave
```

## Usage

<p align="center">
    <a href="https://pypi.python.org">
        <img src="https://ben-nour.com/images/demo.gif" alt="GeoJSON-shave-demo">
    </a>
</p>

Simply pass the file path of your GeoJSON file and it will truncuate the coordinates to 5 decimal places, outputing to the current working directory:

```
$ geojson-shave roads.geoson
```

Alternatively you can specify the number of decimal points you want the coordinates truncuated to:

```
$ geojson-shave roads.geojson -d 3
```

You can also specify if you only want certain Geometry object types in the file to be processed:

```
$ geojson-shave roads.geojson -g LineString Polygon
```

Note that the -g option doesn't apply to objects nested within Geometry Collection.

And to reduce the file size even further you can nullify the property value of Feature objects:

```
$ geojson-shave roads.geojson -p
```

Or select a positive list of properties to keep:

```
$ geojson-shave roads.geojson -kp id,name,level
```

Output to a directory other than the current working directory:

```
$ geojson-shave roads.geojson -o ../data/output.geojson
```
