"""Unit tests for geojson_shave.py"""

import os
import unittest
import sys

from geojson_shave.geojson_shave import (
    _create_coordinates,
    _process_geometry_collection,
    _process_features,
    GEOMETRY_OBJECTS,
)


class TestCreateCoordinates(unittest.TestCase):
    """Tests for the _create_coordinates function.

    Note that both LineStrings' and MultiPoints' coordinates both consist
    of an array of Points, hence only the LineString being tested.
    """

    def setUp(self):
        self.point = {
            "type": "Point",
            "coordinates": [-100.123456, 200.123456],
            "properties": {"name": "Test Point"},
        }

        self.linestring = {
            "type": "LineString",
            "coordinates": [
                [100.123456, 0.123456],
                [101.123456, 1.123456],
                [102.123456, 2.123456],
            ],
        }

        self.multilinestring = {
            "type": "MultiLineString",
            "coordinates": [
                [[-100.123456, 0.123456], [-101.123456, 1.123456]],
                [[102.123456, 2.123456], [103.123456, 3.123456]],
            ],
        }

        self.polygon = {
            "type": "Polygon",
            "coordinates": [
                [
                    [100.123456, 0.123456],
                    [101.123456, 0.123456],
                    [101.123456, 1.123456],
                    [100.123456, 1.123456],
                    [100.123456, 0.123456],
                ]
            ],
        }

        self.multipolygon = {
            "type": "MultiPolygon",
            "coordinates": [
                [
                    [
                        [102.123456, 2.123456],
                        [103.123456, 2.123456],
                        [103.123456, 3.123456],
                        [102.123456, 3.123456],
                        [102.123456, 2.123456],
                    ]
                ],
                [
                    [
                        [100.123456, 0.123456],
                        [101.123456, 0.123456],
                        [101.123456, 1.123456],
                        [100.123456, 1.123456],
                        [100.123456, 0.123456],
                    ],
                    [
                        [100.123456, 0.123456],
                        [100.123456, 0.123456],
                        [100.123456, 0.123456],
                        [100.123456, 0.123456],
                        [100.123456, 0.123456],
                    ],
                ],
            ],
        }

    # Point.
    def test_truncuating_point_coordinates(self):
        """Test that Point coordinates are truncuated succesfully."""
        expected_return_value = [-100.123, 200.123]
        precision = 3
        geometry_coordinates = self.point["coordinates"]
        self.assertEqual(
            _create_coordinates(geometry_coordinates, precision), expected_return_value
        )

    def test_point_same_precision(self):
        """Test that Point coordinates are not truncuated when
        the coordinate decimal points matches what's passed
        to the precision parameter.
        """
        expected_return_value = self.point["coordinates"]
        precision = 6
        geometry_coordinates = self.point["coordinates"]
        self.assertEqual(
            _create_coordinates(geometry_coordinates, precision), expected_return_value
        )

    def test_point_precision_larger_than_places(self):
        """Test that when the precision argument is a value larger
        than the number of coordinate decimnal points, the same coordinate values
        are returned.
        """
        expected_return_value = self.point["coordinates"]
        precision = 50
        geometry_coordinates = self.point["coordinates"]
        self.assertEqual(
            _create_coordinates(geometry_coordinates, precision), expected_return_value
        )

    # LineString.
    def test_truncuating_linestring_coordinates(self):
        """Test that LineString coordinates are truncuated succesfully."""
        expected_return_value = [
            [100.123, 0.123],
            [101.123, 1.123],
            [102.123, 2.123],
        ]
        precision = 3
        geometry_coordinates = self.linestring["coordinates"]
        self.assertEqual(
            _create_coordinates(geometry_coordinates, precision), expected_return_value
        )

    def test_linestring_same_precision(self):
        """Test that LineString coordinates are not truncuated when
        the coordinate decimal points matches what's passed
        to the precision parameter.
        """
        expected_return_value = self.linestring["coordinates"]
        precision = 6
        geometry_coordinates = self.linestring["coordinates"]
        self.assertEqual(
            _create_coordinates(geometry_coordinates, precision), expected_return_value
        )

    def test_linestring_precision_larger_than_places(self):
        """Test that when the precision argument is a value larger
        than the number of coordinate decimnal points, the same coordinate values
        are returned.
        """
        expected_return_value = self.linestring["coordinates"]
        precision = 50
        geometry_coordinates = self.linestring["coordinates"]
        self.assertEqual(
            _create_coordinates(geometry_coordinates, precision), expected_return_value
        )

    # MultiLine strings.
    def test_truncuating_multilinestring_coordinates(self):
        """Test that MultiLineString coordinates are truncuated succesfully."""
        expected_return_value = [
            [[-100.123, 0.123], [-101.123, 1.123]],
            [[102.123, 2.123], [103.123, 3.123]],
        ]
        precision = 3
        geometry_coordinates = self.multilinestring["coordinates"]
        self.assertEqual(
            _create_coordinates(geometry_coordinates, precision), expected_return_value
        )

    def test_multilinestring_precision_larger_than_places(self):
        """Test that when the precision argument is a value larger
        than the number of coordinate decimnal points, the same coordinate values
        are returned.
        """
        expected_return_value = self.multilinestring["coordinates"]
        precision = 50
        geometry_coordinates = self.multilinestring["coordinates"]
        self.assertEqual(
            _create_coordinates(geometry_coordinates, precision), expected_return_value
        )

    def test_multilinestring_same_precision(self):
        """Test that LineString coordinates are not truncuated when
        the coordinate decimal points matches what's passed
        to the precision parameter.
        """
        expected_return_value = self.multipolygon["coordinates"]
        precision = 6
        geometry_coordinates = self.multipolygon["coordinates"]
        self.assertEqual(
            _create_coordinates(geometry_coordinates, precision), expected_return_value
        )

    # Polygon.
    def test_truncuating_polygon_coordinates(self):
        """Test that Polygon coordinates are truncuated succesfully."""
        expected_return_value = [
            [
                [100.123, 0.123],
                [101.123, 0.123],
                [101.123, 1.123],
                [100.123, 1.123],
                [100.123, 0.123],
            ]
        ]
        precision = 3
        geometry_coordinates = self.polygon["coordinates"]
        self.assertEqual(
            _create_coordinates(geometry_coordinates, precision), expected_return_value
        )

    def test_polygon_precision_larger_than_places(self):
        """Test that when the precision argument is a value larger
        than the number of coordinate decimnal points, the same coordinate values
        are returned.
        """
        expected_return_value = [
            [
                [100.123456, 0.123456],
                [101.123456, 0.123456],
                [101.123456, 1.123456],
                [100.123456, 1.123456],
                [100.123456, 0.123456],
            ]
        ]
        precision = 50
        geometry_coordinates = self.polygon["coordinates"]
        self.assertEqual(
            _create_coordinates(geometry_coordinates, precision), expected_return_value
        )

    def test_polygon_same_precision(self):
        """Test that LineString coordinates are not truncuated when
        the coordinate decimal points matches what's passed
        to the precision parameter.
        """
        expected_return_value = [
            [
                [100.123456, 0.123456],
                [101.123456, 0.123456],
                [101.123456, 1.123456],
                [100.123456, 1.123456],
                [100.123456, 0.123456],
            ]
        ]
        precision = 6
        geometry_coordinates = self.polygon["coordinates"]
        self.assertEqual(
            _create_coordinates(geometry_coordinates, precision), expected_return_value
        )

    # MultiPolygon.
    def test_truncuating_multipolygon_coordinates(self):
        """Test that MultiPolygon coordinates are truncuated succesfully."""
        expected_return_value = [
            [
                [
                    [102.123, 2.123],
                    [103.123, 2.123],
                    [103.123, 3.123],
                    [102.123, 3.123],
                    [102.123, 2.123],
                ]
            ],
            [
                [
                    [100.123, 0.123],
                    [101.123, 0.123],
                    [101.123, 1.123],
                    [100.123, 1.123],
                    [100.123, 0.123],
                ],
                [
                    [100.123, 0.123],
                    [100.123, 0.123],
                    [100.123, 0.123],
                    [100.123, 0.123],
                    [100.123, 0.123],
                ],
            ],
        ]
        precision = 3
        geometry_coordinates = self.multipolygon["coordinates"]
        self.assertEqual(
            _create_coordinates(geometry_coordinates, precision), expected_return_value
        )

    def test_multipolygon_precision_larger_than_places(self):
        """Test that when the precision argument is a value larger
        than the number of coordinate decimnal points, the same coordinate values
        are returned.
        """
        expected_return_value = self.multipolygon["coordinates"]
        precision = 50
        geometry_coordinates = self.multipolygon["coordinates"]
        self.assertEqual(
            _create_coordinates(geometry_coordinates, precision), expected_return_value
        )

    def test_multipolygon_same_precision(self):
        """Test that LineString coordinates are not truncuated when
        the coordinate decimal points matches what's passed
        to the precision parameter.
        """
        expected_return_value = self.multipolygon["coordinates"]
        precision = 6
        geometry_coordinates = self.multipolygon["coordinates"]
        self.assertEqual(
            _create_coordinates(geometry_coordinates, precision), expected_return_value
        )


class TestProcessGeometryCollection(unittest.TestCase):
    """Tests for the _process_geometry_collection function."""

    def setUp(self):
        self.geometry_collection = {
            "type": "GeometryCollection",
            "geometries": [
                {"type": "Point", "coordinates": [0.123456, 0.123456]},
                {
                    "type": "LineString",
                    "coordinates": [
                        [1.123456, 1.123456],
                        [2.123456, 3.123456],
                        [4.123456, 5.123456],
                    ],
                },
                {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [6.123456, 6.123456],
                            [8.123456, 8.123456],
                            [10.123456, 10.123456],
                            [6.123456, 6.123456],
                        ]
                    ],
                },
                {
                    "type": "MultiPoint",
                    "coordinates": [
                        [12.123456, 12.123456],
                        [14.123456, 14.123456],
                        [16.123456, 16.123456],
                    ],
                },
            ],
        }

    def test_truncuating_coordinates(self):
        """Tests that the coordinates of each nested Geometry object
        is truncuated correctly."""

        expected_return_value = {
            "type": "GeometryCollection",
            "geometries": [
                {"type": "Point", "coordinates": [0.123, 0.123]},
                {
                    "type": "LineString",
                    "coordinates": [[1.123, 1.123], [2.123, 3.123], [4.123, 5.123]],
                },
                {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [6.123, 6.123],
                            [8.123, 8.123],
                            [10.123, 10.123],
                            [6.123, 6.123],
                        ]
                    ],
                },
                {
                    "type": "MultiPoint",
                    "coordinates": [
                        [12.123, 12.123],
                        [14.123, 14.123],
                        [16.123, 16.123],
                    ],
                },
            ],
        }

        geo_collection = self.geometry_collection
        precision = 3
        self.assertEqual(
            _process_geometry_collection(geo_collection, precision),
            expected_return_value,
        )


class TestProcessFeatures(unittest.TestCase):
    """Tests for the _process_features function."""

    def setUp(self):
        self.feature_collection = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [0.123456, 0.123456]},
                    "properties": {"name": "Feature 1"},
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [5.123456, 5.123456],
                                [15.123456, 5.123456],
                                [15.123456, 15.123456],
                                [5.123456, 15.123456],
                                [5.123456, 5.123456],
                            ]
                        ],
                    },
                    "properties": {"name": "Feature 2"},
                },
            ],
        }
        self.blank_feature_collection = {}

        self.feature = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [100.123456, -0.123456]},
            "properties": {"name": "Example Point"},
        }

    def test_feature_collection_truncuation(self):
        """Test that the coordinates of each nested Geometry object is
        truncuated."""
        geometry_to_include = GEOMETRY_OBJECTS
        precision = 3
        expected_return_value = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [0.123, 0.123]},
                    "properties": {"name": "Feature 1"},
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [5.123, 5.123],
                                [15.123, 5.123],
                                [15.123, 15.123],
                                [5.123, 15.123],
                                [5.123, 5.123],
                            ]
                        ],
                    },
                    "properties": {"name": "Feature 2"},
                },
            ],
        }

        self.assertEqual(
            _process_features(
                self.feature_collection, precision, geometry_to_include, False
            ),
            expected_return_value,
        )

    def test_feature_truncuation(self):
        """Test that the Feature is processed (coordinates truncuated).
        Note the distinction between Feature and FeatureCollection.
        """
        geometry_to_include = GEOMETRY_OBJECTS
        precision = 3
        expected_return_value = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [100.123, -0.123]},
            "properties": {"name": "Example Point"},
        }

        self.assertEqual(
            _process_features(self.feature, precision, geometry_to_include, False),
            expected_return_value,
        )

    def test_empty_gson_file(self):
        """Test that an exception is raised when an empty
        GeoJSON file is passed."""
        with self.assertRaises(RuntimeError):
            _process_features(self.blank_feature_collection, 3, ["Point"], False)

    def test_properties_nullified(self):
        """Test that the properties key returns a null/empty dictionary."""
        precision = 3
        expected_return_value = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [0.123, 0.123]},
                    "properties": {},
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [5.123, 5.123],
                                [15.123, 5.123],
                                [15.123, 15.123],
                                [5.123, 15.123],
                                [5.123, 5.123],
                            ]
                        ],
                    },
                    "properties": {},
                },
            ],
        }

        self.assertEqual(
            _process_features(
                self.feature_collection, precision, GEOMETRY_OBJECTS, True
            ),
            expected_return_value,
        )

    def test_geometry_to_include_parameter(self):
        """Test that only the passed geometry objects are truncuated."""
        geometry_to_include = ["Polygon"]
        precision = 3
        expected_return_value = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [0.123456, 0.123456]},
                    "properties": {"name": "Feature 1"},
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [5.123, 5.123],
                                [15.123, 5.123],
                                [15.123, 15.123],
                                [5.123, 15.123],
                                [5.123, 5.123],
                            ]
                        ],
                    },
                    "properties": {"name": "Feature 2"},
                },
            ],
        }

        self.assertEqual(
            _process_features(
                self.feature_collection, precision, geometry_to_include, False
            ),
            expected_return_value,
        )


if __name__ == "__main__":
    unittest.main(buffer=True)
