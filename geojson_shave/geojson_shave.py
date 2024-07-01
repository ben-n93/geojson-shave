"""A command-line tool that reduces the size of GeoJSON files.
"""

import argparse
from contextlib import suppress
import json
import pathlib

from alive_progress import alive_bar
import humanize

GEOMETRY_OBJECTS = {
    "Point",
    "MultiPoint",
    "LineString",
    "MultiLineString",
    "Polygon",
    "MultiPolygon",
    "GeometryCollection",
}


def get_parser():
    """Create the command-line interface."""
    parser = argparse.ArgumentParser(
        description="""Reduces the size of a GeoJSON file by lowering the
        decimal point precision of the file's latitude/language 
        coordinates.""",
        epilog="""
        EXAMPLES
        --------
        Truncuate a GeoJSON's file to 3 decimal points:
            geojson_shave roads.geojson -d 3

        Only truncuate the coordinates of LineString and Polygon objects:
            geojson_shave roads.geojson -g LineString Polygon

        Replace the properties value with a null value:
            geojson_shave roads.geojson -p
        """,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "input",
        type=argparse.FileType("r"),
        help="Input GeoJSON file to pass to the tool.",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=argparse.FileType("w"),
        help="""Name and path of the output GeoJSON file. Default path is the
        current working directory.""",
        default=pathlib.Path.cwd() / "output.geojson",
        required=False,
    )

    parser.add_argument(
        "-d",
        "--decimal_points",
        type=int,
        help="Number of decimal points to keep when \
                            truncating coordinates. Default is 5.",
        required=False,
        default=5,
    )

    parser.add_argument(
        "-p",
        "--properties",
        help="Overwrite the properties with a null value.",
        required=False,
        action="store_true",
    )

    parser.add_argument(
        "-kp",
        "--keep_properties",
        help="Comma-separated list of property keys. Delete all others.",
        required=False,
        type=lambda s: s.split(',') if s else []
    )


    parser.add_argument(
        "-g",
        "--geometry_object",
        type=str,
        help="""The types of Geometry Object to be processed.
        Default is all objects.""",
        required=False,
        default=GEOMETRY_OBJECTS,
        choices=GEOMETRY_OBJECTS,
        metavar="GEOMETRY_OBJECT",
        nargs="+",
    )

    args = parser.parse_args()
    return args


def create_coordinates(coordinates, precision):
    """Create truncuated coordinates."""
    new_coordinates = []
    for item in coordinates:
        if isinstance(item, list):
            new_coordinates.append(create_coordinates(item, precision))
        else:
            item = round(item, precision)
            new_coordinates.append(float(item))
    return new_coordinates


def process_geometry_collection(geometry_collection, precision):
    """Parse and truncuate the coordinates of each geometry
    object nested within a geometry collection."""
    new_geometry_collection = {"type": "GeometryCollection"}
    processed_geometry_objects = []
    for geometry_object in geometry_collection["geometries"]:
        object_type = geometry_object["type"]
        new_coordinates = create_coordinates(geometry_object["coordinates"], precision)
        processed_geometry_objects.append(
            {"type": object_type, "coordinates": new_coordinates}
        )

    new_geometry_collection["geometries"] = processed_geometry_objects
    return new_geometry_collection


def process_features(geojson, precision, geometry_to_include, keep_properties):
    """Process Feature objects, truncuating coordinates and/or replacing
    the properties member with a blank value."""
    # Create new GeoJSON object.
    if (total_features := geojson.get("features")) is None:
        if geojson.get("type") == "Feature":
            output_geojson = {"type": "Feature"}
            length = 1
        else:
            raise ValueError("Error: there are no Feature objects in this file.")
    else:
        output_geojson = {"type": "FeatureCollection", "features": []}
        length = len(total_features)

    # Process Feature objects.
    with alive_bar(length) as progress_bar:
        progress_bar.title("Processing the input file:")
        if geojson["type"] == "FeatureCollection":
            for index, feature in enumerate(geojson["features"]):
                output_geojson["features"].append(feature)
                if keep_properties is not None:
                    if not keep_properties:
                        output_geojson["features"][index]["properties"] = {}
                    else:
                        for key in output_geojson["features"][index]["properties"].copy():
                            if key not in keep_properties:
                                del output_geojson["features"][index]["properties"][key]
                with suppress(
                    TypeError
                ):  # Feature's "geometry" member has a null value.
                    if (geo_type := feature["geometry"]["type"]) in geometry_to_include:
                        if geo_type == "GeometryCollection":
                            output_geojson["features"][index]["geometry"] = (
                                process_geometry_collection(
                                    feature["geometry"], precision
                                )
                            )
                        else:
                            new_coordinates = create_coordinates(
                                feature["geometry"]["coordinates"], precision
                            )
                            output_geojson["features"][index]["geometry"][
                                "coordinates"
                            ] = new_coordinates
                progress_bar()

        else:  # Only one Feature.
            if geojson["geometry"]["type"] in geometry_to_include:
                new_coordinates = create_coordinates(
                    geojson["geometry"]["coordinates"], precision
                )
                output_geojson["geometry"] = {
                    "type": geojson["geometry"]["type"],
                    "coordinates": new_coordinates,
                }
                if keep_properties is not None:
                    if not keep_properties:
                        output_geojson["properties"] = {}
                    else:
                        for key in output_geojson["features"][index]["properties"].copy():
                            if key not in keep_properties:
                                del output_geojson["features"][index]["properties"][key]
                progress_bar()

    # Including any non-standard (RFC) top-level keys in the output file.
    for key in geojson.keys():
        if key not in ("type", "features", "geometry"):
            output_geojson[key] = geojson[key]
    return output_geojson


def main():
    """Launch the command-line tool."""
    args = get_parser()

    if args.decimal_points < 0:
        raise ValueError(
            """Please only pass a positive number to the decimal argument."""
        )

    if args.properties is True:
        args.keep_properties = []

    # Process input file.
    with open(args.input.name, "r") as input_file:
        try:
            input_geojson = json.load(input_file)
        except json.decoder.JSONDecodeError as e:
            raise ValueError("Error: please provide a valid GeoJSON file.") from e
    output_geojson = process_features(
        input_geojson, args.decimal_points, args.geometry_object, args.keep_properties
    )

    # Write to output file.
    with open(args.output.name, "w", encoding="utf-8") as output_file:
        print("Writing to output file...")
        json.dump(output_geojson, output_file, separators=(",", ":"))

    # Exit message to user.
    size_before = pathlib.Path(args.input.name).stat().st_size
    size_after = pathlib.Path(args.output.name).stat().st_size
    difference = round(((size_before - size_after) / size_before) * 100)
    print(f"Input file size: {humanize.naturalsize(size_before)}.")
    print(f"Output file size: {humanize.naturalsize(size_after)}.")
    print(f"File size reduction: {difference}%")


if __name__ == "__main__":
    main()
