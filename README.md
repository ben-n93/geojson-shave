
<p align="center">
    <a href="https://pypi.python.org">
        <img src="https://ben-nour.com/images/geojson-shave.png" alt="GeoJSON-shave" style="width: 60%; height: auto;"/>
    </a>
</p>

---

geojson-shave reduces the size of GeoJSON files by:

- Truncating latitude/longitude coordinates to the specified decimal places.
- Eliminating unnecessary whitespace.
- (Optionally) replacing the properties key's value with null/empty dictionary.

This tool assumes that your GeoJSON file confirms to the [RFC 7946](https://datatracker.ietf.org/doc/html/rfc7946).

## Installation
```
$ pip install geojson-shave
```

## Usage

Simply pass the file path of your GeoJSON file and it will truncuate the coordinates to 5 decimal places, outputing to the current working directory:

```
$ geojson-shave roads.geoson
```

Alterntatively you can specify the number of decimal points you want the coordiantes truncuated to:

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

Output to a directory other than the current working directory:
```
$ geojson-shave roads.geojson -o ../data/output.geojson
```

## TODO

- [ ] Add support for passing the URL of a hosted GeoJSON file to the tool.
