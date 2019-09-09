import re

# Static config for the wms metadata.
# pylint: skip-file

response_cfg = {
    "Access-Control-Allow-Origin": "*",  # CORS header
}


service_cfg = {
    ## Which web service(s) should be supported by this instance
    # Defaults: wms: True, wcs: False, wmts: False
    # Notes:
    #   WMTS support is implemented as a thin proxy to WMS. Some corners of the spec are interpreted
    #   somewhat loosely. In particular exception documents are directly translated from the underlying
    #   WMS error and are unlikely to be fully compliant with the WMTS standard.
    "wcs": True,
    "wms": True,
    "wmts": True,

    ## Required config for WMS and/or WCS
    # Service title - appears e.g. in Terria catalog
    "title": "GEOGLAM WMS",
    # Service URL.  Should a fully qualified URL or a list of fully qualified URLs that the service can return
    # in the GetCapabilities document based on the requesting url
    "url": [ "http://ows.easi-eo.solutions/" ],
    # URL that humans can visit to learn more about the WMS or organization
    # should be fully qualified
    "human_url": "http://csiro.au",
    # Supported co-ordinate reference systems
    "published_CRSs": {
        "EPSG:3857": {  # Web Mercator
            "geographic": False,
            "horizontal_coord": "x",
            "vertical_coord": "y",
        },
        "EPSG:4326": {  # WGS-84
            "geographic": True,
            "vertical_coord_first": True
        },
        "EPSG:3577": {  # GDA-94, internal representation
            "geographic": False,
            "horizontal_coord": "x",
            "vertical_coord": "y",
        },
    },

    ## Required config for WCS
    # Must be a geographic CRS in the published_CRSs list.  EPSG:4326 is recommended, but any geographic CRS should work.
    "default_geographic_CRS": "EPSG:4326",

    # Supported WCS formats
    "wcs_formats": {
        # Key is the format name, as used in DescribeCoverage XML
        "GeoTIFF": {
            # Renderer is the FQN of a Python function that takes:
            #   * A WCSRequest object
            #   * Some ODC data to be rendered.
            "renderer": "datacube_wms.wcs_utils.get_tiff",
            # The MIME type of the image, as used in the Http Response.
            "mime": "image/geotiff",
            # The file extension to add to the filename.
            "extension": "tif",
            # Whether or not the file format supports multiple time slices.
            "multi-time": False
        },
        "netCDF": {
            "renderer": "datacube_wms.wcs_utils.get_netcdf",
            "mime": "application/x-netcdf",
            "extension": "nc",
            "multi-time": True,
        }
    },
    # The native wcs format must be declared in wcs_formats above.
    "native_wcs_format": "GeoTIFF",

    ## Optional config for instances supporting WMS
    # Max tile height/width.  If not specified, default to 256x256
    "max_width": 512,
    "max_height": 512,

    # Optional config for all services (WMS and/or WCS) - may be set to blank/empty, no defaults
    "abstract": """GEOGALM OGC Web Services""",
    "keywords": [
        "fractional cover",
        "australia",
        "time-series",
    ],
    "contact_info": {
        "person": "Robert Woodcock",
        "organisation": "CSIRO",
        "position": "EASI Hub Coordinator",
        "address": {
            "type": "postal",
            "address": "CSIRO Black Mountain Laboratories, Clunies Ross Street",
            "city": "Black Mountain",
            "state": "ACT",
            "postcode": "2601",
            "country": "Australia",
        },
        "telephone": "+61 2 6246 5521",
        "email": "Robert.Woodcock@csiro.au",
    },
    "fees": "",
    "access_constraints": "",
    # If True this will not calculate spatial extents
    # in update_ranges.py but will instead use a default
    # extent covering much of Australia for all
    # temporal extents
    # False by default (calculate spatial extents)
    # "use_default_extent": False,
    # If using GeoTIFFs as storage
    # this will set the rasterio env
    # GDAL Config for GTiff Georeferencing
    # See https://www.gdal.org/frmt_gtiff.html#georeferencing
    # "geotiff_georeference_source": "INTERNAL",
    # Attribution.  This entire section is optional.  If provided, it is taken as the
    #               default attribution for any layer that does not override it.
    "attribution": {
        # Attribution must contain at least one of ("title", "url" and "logo")
        # A human readable title for the attribution - e.g. the name of the attributed organisation
        "title": "CSIRO",
        # The associated - e.g. URL for the attributed organisation
        "url": "http://www.csiro.au",
        # Logo image - e.g. for the attributed organisation
        "logo": {
            # Image width in pixels (optional)
            "width": 73,
            # Image height in pixels (optional)
            "height": 73,
            # URL for the logo image. (required if logo specified)
            "url": "https://www.csiro.au/~/media/Web-team/Images/CSIRO_Logo/CSIRO_Logo.png",
            # Image MIME type for the logo - should match type referenced in the logo url (required if logo specified.)
            "format": "image/png",
        }
    },
    # These define the AuthorityURLs.  They represent the authorities that define the layer "Identifiers" below.
    # The spec allows AuthorityURLs to be defined anywhere on the Layer heirarchy, but datacube_ows treats them
    # as global entities.
    "authorities": {
        # The authorities dictionary maps names to authority urls.
        "csiro": "https://www.csiro.au",
    }
}

layer_cfg = [
    # Layer Config is a list of platform configs
    {
        # Name and title of the platform layer.
        # Platform layers are not mappable. The name is for internal server use only.
        "name": "FRACTIONAL_COVER",
        "title": "Fractional Cover",
        "abstract": "Fractional cover products derived from MODIS data",

        # Attribution.  This entire section is optional.  If provided, it overrides any
        #               attribution defined in the service_cfg for all layers under this
        #               platform that do not define their own attribution.
        "attribution": {
            # Attribution must contain at least one of ("title", "url" and "logo")
            # A human readable title for the attribution - e.g. the name of the attributed organisation
            "title": "CSIRO",
            # The associated - e.g. URL for the attributed organisation
            "url": "http://www.csiro.au",
            # Logo image - e.g. for the attributed organisation
            "logo": {
                # Image width in pixels (optional)
                "width": 73,
                # Image height in pixels (optional)
                "height": 73,
                # URL for the logo image. (required if logo specified)
                "url": "https://www.csiro.au/~/media/Web-team/Images/CSIRO_Logo/CSIRO_Logo.png",
                # Image MIME type for the logo - should match type referenced in the logo url (required if logo specified.)
                "format": "image/png",
            }
        },

        # Products available for this platform.
        # For each product, the "name" is the Datacube name, and the label is used
        # to describe the label to end-users.
        "products": [
            {
                # Included as a keyword  for the layer
                "label": "frac_cover_monthly",
                # Included as a keyword  for the layer
                "type": "fractional cover",
                # Included as a keyword  for the layer
                "variant": "three band",
                # The WMS name for the layer
                "name": "frac_cover",
                # The Datacube name for the associated data product
                "product_name": "frac_cover",
                # The Datacube name for the associated pixel-quality product (optional)
                # The name of the associated Datacube pixel-quality product
                # "pq_dataset": "ls8_pq_albers",
                # The name of the measurement band for the pixel-quality product
                # (Only required if pq_dataset is set)
                #"pq_band": "pixel_qa",
                # Supported bands, mapping native band names to a list of possible aliases.
                # 1. Aliases must be unique for the product.
                # 2. Band aliases can be used anywhere in the configuration that refers to bands by name.
                # 3. The native band name MAY be explicitly declared as an alias for the band, but are always treated as
                # a valid alias.
                # 4. The band labels used in GetFeatureInfo and WCS responses will be the first declared alias (or the native name
                # if no aliases are declared.)
                # 5. Bands NOT listed here will not be included in the GetFeatureInfo output and cannot be referenced
                # elsewhere in the configuration.
                # 6. If not specified for a product, defaults to all available bands, using only their native names.
                "bands": {
                    "bare_soil": [],
                    "phot_veg": [],
                    "nphot_veg": [],
                },
                # Min zoom factor - sets the zoom level where the cutover from indicative polygons
                # to actual imagery occurs.
                "min_zoom_factor": 15.0,
                # Min zoom factor (above) works well for small-tiled requests, (e.g. 256x256 as sent by Terria).
                # However, for large-tiled requests (e.g. as sent by QGIS), large and intensive queries can still
                # go through to the datacube.
                # max_datasets_wms specifies a maximum number of datasets that a GetMap request can retrieve.
                # Indicatative polygons are displayed if a request exceeds the limits imposed by EITHER max_dataset_wms
                # OR min_zoom_factor.
                # max_datasets_wms should be set in conjunction with min_zoom_factor so that Terria style 256x256
                # tiled requests respond consistently - you never want to see a mixture of photographic tiles and polygon
                # tiles at a given zoom level.  i.e. max_datasets_wms should be greater than the number of datasets
                # required for most intensive possible photographic query given the min_zoom_factor.
                # Note that the ideal value may vary from product to product depending on the size of the dataset
                # extents for the product.
                # Defaults to zero, which is interpreted as no dataset limit.
                # 6 seems to work with a min_zoom_factor of 500.0 for "old-style" Net-CDF albers tiled data.
                "max_datasets_wms": 12,
                # max_datasets_wcs is the WCS equivalent of max_datasets_wms.  The main requirement for setting this
                # value is to avoid gateway timeouts on overly large WCS requests (and reduce server load).
                "max_datasets_wcs": 16,
                # The fill-colour of the indicative polygons when zoomed out.
                # Triplets (rgb) or quadruplets (rgba) of integers 0-255.
                "zoomed_out_fill_colour": [150, 180, 200, 160],
                # Extent mask function
                # Determines what portions of dataset is potentially meaningful data.
                # Multiple extent mask functions are supported - see USGS Level 1 example below.
                #
                # Three formats are supported:
                # 1. A function object or lambda
                #    e.g. "extent_mask_func": lambda data, band: (data[band] != data[band].attrs['nodata']),
                #
                # 2. A string containing a fully qualified path to a python function (e.g. as shown below)
                #
                # 3. A dict containing the following elements:
                #    a) "function" (required): A string containing the fully qualified path to a python function
                #    b) "args" (optional): An array of additional positional arguments that will always be passed to the function.
                #    c) "kwargs" (optional): An array of additional keyword arguments that will always be passed to the function.
                #    d) "pass_product_cfg" (optional): Boolean (defaults to False). If true, the relevant ProductLayerConfig is passed
                #       to the function as a keyword argument named "product_cfg".  This is useful if you are passing band aliases
                #       to the function in the args or kwargs.  The product_cfg allows the index function to convert band aliases to
                #       to band names.
                #
                # The function is assumed to take two arguments, data (an xarray Dataset) and band (a band name).  (Plus any additional
                # arguments required by the args and kwargs values in format 3, possibly including product_cfg.)
                #
                "extent_mask_func": "datacube_wms.ogc_utils.mask_by_val",
                # Fuse func
                # Determines how multiple dataset arrays are compressed into a single time array
                # All the formats described above for "extent_mask_func" are supported here as well.
                #"fuse_func": None,
                # PQ Fuse func
                # Determines how multiple dataset arrays are compressed into a single time array for the PQ layer
                # All the formats described above for "extent_mask_func" are supported here as well.
                #"pq_fuse_func": None,
                # PQ Ignore time
                # Doesn't use the time from the data to find a corresponding mask layer
                # Used when you have a mask layer that doesn't have time
                "pq_ignore_time": False,
                # Flags listed here are ignored in GetFeatureInfo requests.
                # (defaults to empty list)
                "ignore_info_flags": [],
                "legend": {
                    "styles": ["simple_rgb", "bare_soil", "phot_veg", "nphot_veg", "tot_cover"]
                }, 
                # Include an additional list of utc dates in the WMS Get Feature Info
                # HACK: only used for GSKY non-solar day lookup
                "feature_info_include_utc_dates": False,
                # Set to true if the band product dataset extents include nodata regions.
                "data_manual_merge": False,
                # Set to true if the pq product dataset extents include nodata regions.
                # "pq_manual_merge": False,
                # Bands to always fetch from the Datacube, even if it is not used by the active style.
                # Useful for when a particular band is always needed for the extent_mask_func,
                "always_fetch_bands": [ ],
                # Apply corrections for solar angle, for "Level 1" products.
                # (Defaults to false - should not be used for NBAR/NBAR-T or other Analysis Ready products
                "apply_solar_corrections": False,
                # If this value is set then WCS works exclusively with the configured
                # date and advertises no time dimension in GetCapabilities.
                # Intended mostly for WCS debugging.
                # "wcs_sole_time": "2017-01-01",
                # The default bands for a WCS request.
                # 1. Must be provided if WCS is activated.
                # 2. Must contain at least one band.
                # 3. All bands must exist
                # 4. Bands may be referred to by either native name or alias
                "wcs_default_bands": [ "bare_soil", "phot_veg", "nphot_veg" ],
                # The "native" CRS for WCS.
                # Can be omitted if the product has a single native CRS, as this will be used in preference.
                "native_wcs_crs": "EPSG:3577",
                # The resolution (x,y) for WCS.
                # This is the number of CRS units (e.g. degrees, metres) per pixel in the horizontal and vertical
                # directions for the native resolution.  E.g. for a EPSG:3577  (25.0,25.0) for Landsat-8 and (10.0,10.0 for Sentinel-2)
                "native_wcs_resolution": [ 500.0, 500.0 ],
                # FeatureListURLs and DataURLs are optional.
                # Multiple of each may be defined per product.
                # FeatureListURLs point to "a list of the features represented in a Layer".
                # DataURLs "offer a link to the underlying data represented by a particular layer"
                
                # Styles.
                #
                # See band_mapper.py
                #
                # The various available spectral bands, and ways to combine them
                # into a single rgb image.
                # The examples here are ad hoc
                #
                # LS7:  http://www.indexdatabase.de/db/s-single.php?id=8
                # LS8:  http://www.indexdatabase.de/db/s-single.php?id=168
                "styles": [
                    # Examples of styles which are linear combinations of the available spectral bands.
                    #
                    {
                        "name": "simple_rgb",
                        "title": "Simple RGB",
                        "abstract": "Simple true-colour image using bare soil, photo and non photo synthetic vegetatation as RGB",
                        "components": {
                            # The component keys MUST be "red", "green" and "blue" (and optionally "alpha")
                            "red": {
                                # Band aliases may be used here.
                                "bare_soil": 1.0
                            },
                            "green": {
                                "phot_veg": 1.0
                            },
                            "blue": {
                                "nphot_veg": 1.0
                            }
                        },
                        "legend": {
                            "url": "http://www-data.wron.csiro.au/remotesensing/MODIS/products/public/misc/rgb_geoglam.png",
                            },
                        # The raw band value range to be compressed to an 8 bit range for the output image tiles.
                        # Band values outside this range are clipped to 0 or 255 as appropriate.
                        "scale_range": [0.0, 111.0]
                    },
                    {
                        "name": "bare_soil",
                        "title": "Bare Soil",
                        "abstract": "Bare Soil",
                        "legend": {
                            "url": "http://www-data.wron.csiro.au/remotesensing/MODIS/products/public/misc/bare_Vegetation_cover.png",
                            },
                        "needed_bands": ["bare_soil"],
                         "color_ramp": [
                            {
                                "value": -0.0,
                                "color": "#FFF5F0",
                                "alpha": 0.0,
                            },
                            {
                                "value": 0.0,
                                "color": "#FFF5F0",
                                "alpha": 1.0,
                            },
                            {
                                "value": 10.0,
                                "color": "#FFF5F0",
                            },
                            {
                                "value": 20.0,
                                "color": "#FEE1D4",
                            },
                            {
                                "value": 30.0,
                                "color": "#FCC1A9",
                            },
                            {
                                "value": 40.0,
                                "color": "#FC9C7E",
                            },
                            {
                                "value": 50.0,
                                "color": "#FB7757",
                            },
                            {
                                "value": 60.0,
                                "color": "#F44F38",
                            },
                            {
                                "value": 70.0,
                                "color": "#DE2B25",
                            },
                            {
                                "value": 80.0,
                                "color": "#BD141A",
                            },
                            {
                                "value": 90.0,
                                "color": "#980B13",
                            },
                            {
                                "value": 100.0,
                                "color": "#67000D",
                            }
                        ],
                        "scale_range": [0.0, 111.0]
                    },
                    {
                        "name": "phot_veg",
                        "title": "Photosynthetic Vegetation",
                        "abstract": "Photosyntehtic Vegetation",
                        "legend": {
                            "url": "http://www-data.wron.csiro.au/remotesensing/MODIS/products/public/misc/green_Vegetation_cover.png",
                            },
                        "needed_bands": ["phot_veg"],
                        "color_ramp": [
                            {
                                "value": -0.0,
                                "color": "#F7FCFD",
                                "alpha": 0.0,
                            },
                            {
                                "value": 0.0,
                                "color": "#F7FCFD",
                                "alpha": 1.0,
                            },
                            {
                                "value": 10.0,
                                "color": "#F7FCFD",
                            },
                            {
                                "value": 20.0,
                                "color": "#E6F5F9",
                            },
                            {
                                "value": 30.0,
                                "color": "#D0EDE9",
                            },
                            {
                                "value": 40.0,
                                "color": "#A6DDD0",
                            },
                            {
                                "value": 50.0,
                                "color": "#77C9B0",
                            },
                            {
                                "value": 60.0,
                                "color": "#50B689",
                            },
                            {
                                "value": 70.0,
                                "color": "#339E5F",
                            },
                            {
                                "value": 80.0,
                                "color": "#16803B",
                            },
                            {
                                "value": 90.0,
                                "color": "#006428",
                            },
                            {
                                "value": 100.0,
                                "color": "#00441B",
                            }
                        ],
                        "scale_range": [0.0, 110.0]
                    },
                    {
                        "name": "nphot_veg",
                        "title": "Non-photosynthetic vegetation",
                        "abstract": "Non-photosynthetic vegetation",
                        "legend": {
                            "url": "http://www-data.wron.csiro.au/remotesensing/MODIS/products/public/misc/nongreen_Vegetation_cover.png",
                            },
                        "needed_bands": ["nphot_veg"],
                        "color_ramp": [
                            {
                                "value": -0.0,
                                "color": "#F7FBFF",
                                "alpha": 0.0,
                            },
                            {
                                "value": 0.0,
                                "color": "#F7FBFF",
                                "alpha": 1.0,
                            },
                            {
                                "value": 10.0,
                                "color": "#F7FBFF",
                            },
                            {
                                "value": 20.0,
                                "color": "#E0ECF7",
                            },
                            {
                                "value": 30.0,
                                "color": "#CADDF0",
                            },
                            {
                                "value": 40.0,
                                "color": "#A8CEE4",
                            },
                            {
                                "value": 50.0,
                                "color": "#7CB7D9",
                            },
                            {
                                "value": 60.0,
                                "color": "#539ECC",
                            },
                            {
                                "value": 70.0,
                                "color": "#3383BE",
                            },
                            {
                                "value": 80.0,
                                "color": "#1765AB",
                            },
                            {
                                "value": 90.0,
                                "color": "#084A91",
                            },
                            {
                                "value": 100.0,
                                "color": "#08306B",
                            }
                        ],
                        "scale_range": [0.0, 111.0]
                    },
                    {
                        "name": "tot_cover",
                        "title": "Total Cover",
                        "abstract": "This layer is created after combining with photo synthetic vegetation and non synthetic vegetation",
                        "legend": {
                            "url": "http://www-data.wron.csiro.au/remotesensing/MODIS/products/public/misc/Total_Vegetation_cover.png",
                            },
                        "index_function": {
                            "function": lambda data: data["phot_veg"] + data["nphot_veg"],
                        },
                        "needed_bands": ["phot_veg","nphot_veg"],
                        "color_ramp": [
                            # Any value less than the first entry will have colour and alpha of the first entry.
                            # (i.e. in this example all negative values will be fully transparent (alpha=0.0).)
                            {
                                "value": -0.0,
                                "color": "#543005",
                                "alpha": 0.0,
                            },
                            {
                                "value": 0.0,
                                "color": "#543005",
                                "alpha": 1.0,
                            },
                            {
                                "value": 10.0,
                                "color": "#543005",
                            },
                            {
                                "value": 20.0,
                                "color": "#91560E",
                            },
                            {
                                "value": 30.0,
                                "color": "#C6903F",
                            },
                            {
                                "value": 40.0,
                                "color": "#E7CF95",
                            },
                            {
                                "value": 50.0,
                                "color": "#F5EEDA",
                            },
                            {
                                "value": 60.0,
                                "color": "#DAEEEB",
                            },
                            {
                                "value": 70.0,
                                "color": "#98D6CD",
                            },
                            {
                                "value": 80.0,
                                "color": "#45A39A",
                            },
                            {
                                "value": 90.0,
                                "color": "#0A6F67",
                            },
                            {
                                "value": 100.0,
                                "color": "#004035",
                            },
                            # Values greater than the last entry will use the colour and alpha of the last entry.
                            # (N.B. This will not happen for this example because it is normalised so that 1.0 is
                            # maximum possible value.)
                            {
                                "value": 111.0,
                                "color": "#004035",
                                "alpha" : 0.0
                            }
                        ],
                        "scale_range": [0.0, 110.0]
                    },
                ],
                # Default style (if request does not specify style)
                # MUST be defined in the styles list above.

                # (Looks like Terria assumes this is the first style in the list, but this is
                #  not required by the standard.)
                "default_style": "simple_rgb",

                # Attribution.  This entire section is optional.  If not provided, the default attribution
                #               from the parent platform or the service config is used.
                #               If no attribution is defined at any level, no attribution will be published.
                "attribution": {
                    # Attribution must contain at least one of ("title", "url" and "logo")
                    # A human readable title for the attribution - e.g. the name of the attributed organisation
                    "title": "GEOGLAM Fractional Cover",
                    # The associated - e.g. URL for the attributed organisation
                    "url": "http://www.csiro.au",
                    # Logo image - e.g. for the attributed organisation
                    "logo": {
                        # Image width in pixels (optional)
                        "width": 73,
                        # Image height in pixels (optional)
                        "height": 73,
                        # URL for the logo image. (required if logo specified)
                        "url": "https://www.csiro.au/~/media/Web-team/Images/CSIRO_Logo/CSIRO_Logo.png",
                        # Image MIME type for the logo - should match type referenced in the logo url (required if logo specified.)
                        "format": "image/png",
                    }
                }
            },
        ],
    }
]



