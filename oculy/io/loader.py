# --------------------------------------------------------------------------------------
# Copyright 2020 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Interface for data loaders.

"""
from typing import Dict as TypedDict
from typing import Sequence

from atom.api import Callable, Dict, Int, List, Str
from enaml.core.api import Declarative, d_, d_func
from glaze.utils.atom_util import HasPreferencesAtom
from xarray import Dataset

from oculy.transformations.masks import MaskSpecification


class DataKeyError(KeyError):
    """Custom KeyError raised when one required data does not exist in the dataset."""

    def __init__(self, missing, existing):
        self.missing = missing
        self.existing = existing

    def __str__(self):
        return (
            "The following names are not present in the dataset: "
            f"{self.missing}. Existing names are: {self.existing}"
        )


# NOTE use an actual instance as a base to store preferences (Dict per id on plugin)
class BaseLoader(HasPreferencesAtom):
    """"""

    #: Path to the on-disk file storing the data
    path = Str()

    #: Content of the file (i.e. names, data shape etc)
    # TODO formalize the format of this as possible usage are more clearly identified
    content = Dict()

    #: Maximal size in (MB) a loader is allowed to keep in cache.
    #: Keeping data in cache will improve performance but degrade memory usage.
    caching_limit = Int(100).tag(pref=True)

    #: Callable taking care of applying any in-memory masking required and taking
    #: the data to be masked, the data to generate the mask and the mask
    #: specification for each mask source data.
    #: Callable[ [Dataset, Dataset, TypedDict[str, MaskSpecification]], Dataset ]
    mask_data = Callable()

    # FIXME formalize the filtering format keeping something compatible with out of
    # memory filtering
    # HDF5 files are also a concern (store more than 1D data)
    def load_data(
        self,
        names: Sequence[str],
        masks: TypedDict[str, MaskSpecification],
    ) -> Dataset:
        """Load data from the on-disk resource.

        Parameters
        ----------
        names : Sequence[str]
            Names-like string referring to the content of the file.
        masks : TypedDict[str, MaskSpecification]
            Mapping of mapping operation to perform on the specified named data, the
            resulting mask are applied to the requested data (see `names`)

        Returns
        -------
        Dataset
            xarray Dataset containing the requested data.

        Raises
        ------
        DataKeyError
            Raised if the name of some data or mask is not found in the on disk store.

        """
        raise NotImplementedError

    def determine_content(self, details=False) -> None:
        raise NotImplementedError

    def clear(self) -> None:
        """Clear any known information about the data file."""
        pass


class Loader(Declarative):
    """"""

    #: Unique ID of the loader
    id = d_(Str())

    #: Supported file extensions for the loader
    #: If multiple loaders support the same extension the user will be allowed
    #: to pick the relevant one.
    file_extensions = d_(List())

    @d_func
    def get_cls(self) -> BaseLoader:
        raise NotImplementedError
