# --------------------------------------------------------------------------------------
# Copyright 2020 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""CSV data loader.

Requires Pandas for fast IO.

"""
import csv
from typing import Mapping, Sequence

from atom.api import Bool, Str, Typed
from pandas import read_csv
from xarray import Dataset

from oculy.transformations import MaskSpecification

from ...loader import BaseLoader, DataKeyError


# TODO add support for adding units
class CSVLoader(BaseLoader):
    """Load data stored in a csv file.

    The system can automatically strip comment and determine
    the proper delimiter.

    """

    #: Should data file be loaded all at once or should only
    # the relevant columns
    #: be loaded.
    eager_load = Bool(True).tag(pref=True)

    #: Column delimiter, an empty string means that the separator
    # should be inferred
    delimiter = Str("").tag(pref=True)

    #: Character marking a comment, fully commented lines are
    # ignored
    comment = Str("#").tag(pref=True)

    def load_data(
        self,
        columns: Sequence[str],
        masks: Mapping[str, MaskSpecification],
    ) -> Dataset:
        """Load data from the CSV file.

        Parameters
        ----------
        names : Sequence[str]
            Names-like string referring to the content of the file.
        masks : Mapping[str, MaskSpecification]
            Mapping of mapping operation to perform on the specified
            named data, the resulting mask are applied to the requested
            data (see `names`) apply_mask : Callable[ [Dataset, Dataset,
            Mapping[str, MaskSpecification]], Dataset ]
            allable taking care of applying any in-memory masking required
            and taking the data to be masked, the data to generate the mask
            and the mask specification for each mask source data.

        Returns
        -------
        Dataset
            xarray Dataset containing the requested data.

        Raises
        ------
        DataKeyError
            Raised if the name of some data or mask is not found in the
            on disk store.

        """
        required = list(columns) + list(masks)
        if not self.content:
            self.determine_content()

        if any(r not in self.content for r in required):
            raise DataKeyError(
                [r for r in required if r not in self.content], self.content
            )

        if not self._data:
            self._data = read_csv(
                self.path,
                sep=self.delimiter or None,
                comment=self.comment,
                usecols=required if self.eager_load else None,
                engine="c" if self.delimiter else "python",
            ).to_xarray()
        else:
            missing = [r for r in required if r not in self._data]
            if missing:
                self._data.update(
                    read_csv(
                        self.path,
                        sep=self.delimiter or None,
                        comment=self.comment,
                        usecols=missing,
                        engine="c" if self.delimiter else "python",
                    ).to_xarray()
                )

        data = self._data[columns]
        if masks:
            data = self.mask_data(data, self._data[list(masks)], masks)

        if self._data.nbytes > self.caching_limit * 1e6:
            del self._data

        return data

    def determine_content(self, details: bool = False) -> None:
        """Determine the name of the columns."""
        if self.content:
            return

        with open(self.path, "r") as f:
            line = f.readline()
            while line.strip().startswith(self.comment):
                line = f.readline()

        sep = self.delimiter or csv.Sniffer().sniff(line).delimiter
        self.content = dict.fromkeys([n.strip() for n in line.split(sep)])

    def clear(self):
        """Delete content and any cached data."""
        del self.content
        del self._data

    # --- Private API --------------------------------------------------------

    #: Cached content of the file. Will be preserved only if its size does not
    #: exceed the maximum allowed cache size.
    _data = Typed(Dataset)
