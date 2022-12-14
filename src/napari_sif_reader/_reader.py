"""
This module is an example of a barebones numpy reader plugin for napari.

It implements the Reader specification, but your plugin may choose to
implement multiple readers or even other plugin contributions. see:
https://napari.org/stable/plugins/guides.html?#readers
"""
import sif_parser


def napari_get_reader(path):
    """A basic implementation of a Reader contribution.

    Parameters
    ----------
    path : str or list of str
        Path to file, or list of paths.

    Returns
    -------
    function or None
        If the path is a recognized format, return a function that accepts the
        same path or list of paths, and returns a list of layer data tuples.
    """
    if isinstance(path, list):
        # reader plugins may be handed single path, or a list of paths.
        # if it is a list, it is assumed to be an image stack...
        # so we are only going to look at the first file.
        path = path[0]

    # if we know we cannot read the file, we immediately return None.
    if not path.endswith(".sif"):
        return None

    # otherwise we return the *function* that can read ``path``.
    return reader_function

def get_custome_metadata_func(info_sif_reader):
    metadata_key_names = ['SifVersion',
                                'ExperimentTime',
                                'DetectorTemperature',
                                'ExposureTime',
                                'CycleTime',
                                'AccumulatedCycleTime',
                                'AccumulatedCycles',
                                'StackCycleTime',
                                'PixelReadoutTime',
                                'GainDAC',
                                'DetectorType',
                                'DetectorDimensions',
                                'OriginalFilename',
                                'ShutterTime',
                                'spectrograph',
                                'SifCalbVersion',
                                'Calibration_data',
                                'FrameAxis',
                                'DataType',
                                'ImageAxis',
                                'NumberOfFrames',
                                'NumberOfSubImages',
                                'TotalLength',
                                'ImageLength',
                                'xbin',
                                'ybin']
    metadata_dict_output = {}
    
    
    for key in range(len(metadata_key_names)):
        metadata_dict_output[metadata_key_names[key]] = info_sif_reader.get(metadata_key_names[key])
        
    return metadata_dict_output

def reader_function(path):
    """Take a path or list of paths and return a list of LayerData tuples.

    Readers are expected to return data as a list of tuples, where each tuple
    is (data, [add_kwargs, [layer_type]]), "add_kwargs" and "layer_type" are
    both optional.

    Parameters
    ----------
    path : str or list of str
        Path to file, or list of paths.

    Returns
    -------
    layer_data : list of tuples
        A list of LayerData tuples where each tuple in the list contains
        (data, metadata, layer_type), where data is a numpy array, metadata is
        a dict of keyword arguments for the corresponding viewer.add_* method
        in napari, and layer_type is a lower-case string naming the type of
        layer. Both "meta", and "layer_type" are optional. napari will
        default to layer_type=="image" if not provided
    """
    # handle both a string and a list of strings
    paths = [path] if isinstance(path, str) else path
    # load all files into array
    # arrays = [np.load(_path) for _path in paths]
    # stack arrays into single array
    data, info = sif_parser.np_open(path)
    metadata = get_custome_metadata_func(info)

    
    #################### note: update this to only get usefulll 
    ########## and not redudndant metadata info

    # meta = dict(info)

    # optional kwargs for the corresponding viewer.add_* method
    add_kwargs = {
        "colormap" : "twilight_shifted",
        "gamma" : 0.15,
        "metadata": metadata
    }

    layer_type = "image"  # optional, default is "image"
    return [(data, add_kwargs, layer_type)]
