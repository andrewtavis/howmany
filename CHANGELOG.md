# Changelog

howmany tries to follow [semantic versioning](https://semver.org/), a MAJOR.MINOR.PATCH version where increments are made of the:

- MAJOR version when we make incompatible API changes
- MINOR version when we add functionality in a backwards compatible manner
- PATCH version when we make backwards compatible bug fixes

# howmany 0.2.0

- The user can now pass predefined amounts, labels and units to `howmany.compare()`.
- Default values were removed from `howmany.compare()`.
- The example Jupyter notebook and examples in the readme were expanded to show v0.2.0 functionality.
- Minor bugs were fixed for unit conversions and checking whether units are `None`.

# howmany 0.1.0

- The main function `howmany.compare()` has Wikidata QIDs and properties passed to it and returns a dictionary of labels and the ratio between the property values.
- Labels can be returned in any language given the `iso` argument of `howmany.compare()`.
- Allows for comparing area that are in square kilometers as well as meters via length and width properties.
- Basic unit and dimension conversions have been added.
- Wikidata REST API functions have been made for easy data statement access.
- A utility function has been added to convert floats to strings so people can more easily display how small something is in comparison to another.
