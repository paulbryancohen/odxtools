<<<<<<< HEAD
# SPDX-License-Identifier: MIT
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union
from xml.etree import ElementTree

from .basecomparam import BaseComparam
from .nameditemlist import NamedItemList
from .odxlink import OdxDocFragment, OdxLinkDatabase, OdxLinkId
from .odxtypes import odxstr_to_bool

if TYPE_CHECKING:
    from .diaglayer import DiagLayer

ComplexValue = List[Union[str, "ComplexValue"]]


def create_complex_value_from_et(et_element: ElementTree.Element) -> ComplexValue:
    result: ComplexValue = []
    for el in et_element:
        if el.tag == "SIMPLE-VALUE":
            result.append("" if el.text is None else el.text)
        else:
            result.append(create_complex_value_from_et(el))
    return result


@dataclass
class ComplexComparam(BaseComparam):
    comparams: NamedItemList[BaseComparam]
    complex_physical_default_value: Optional[ComplexValue]
    allow_multiple_values_raw: Optional[bool]

    @property
    def allow_multiple_values(self) -> bool:
        return self.allow_multiple_values_raw is True

    @staticmethod
    def from_et(et_element: ElementTree.Element,
                doc_frags: List[OdxDocFragment]) -> "ComplexComparam":
        # create an "empty" ComplexComparam object without calling the
        # "official" constructor. We need to do this because we need
        # all data attributes of the class to call the constructor,
        # including those which are supposed to be handled by the base
        # class (i.e., ComparamBase)
        result = ComplexComparam.__new__(ComplexComparam)

        # initialize the new "empty" object from the ElementTree
        result.__init_from_et__(et_element, doc_frags)

        return result

    def __init_from_et__(self, et_element: ElementTree.Element,
                         doc_frags: List[OdxDocFragment]) -> None:
        super().__init_from_et__(et_element, doc_frags)

        # to avoid a cyclic import, create_any_comparam_from_et cannot
        # be imported globally. TODO: figure out if this has
        # performance implications
        from .createanycomparam import create_any_comparam_from_et

        self.comparams = NamedItemList()
        for cp_el in et_element:
            if cp_el.tag in ("COMPARAM", "COMPLEX-COMPARAM"):
                self.comparams.append(create_any_comparam_from_et(cp_el, doc_frags))

        self.complex_physical_default_value = None
        if cpdv_elem := et_element.find("COMPLEX-PHYSICAL-DEFAULT-VALUE"):
            self.complex_physical_default_value = create_complex_value_from_et(cpdv_elem)

        self.allow_multiple_values_raw = odxstr_to_bool(et_element.get("ALLOW-MULTIPLE-VALUES"))

    def _build_odxlinks(self) -> Dict[OdxLinkId, Any]:
        odxlinks = super()._build_odxlinks()
        for comparam in self.comparams:
            odxlinks.update(comparam._build_odxlinks())
        return odxlinks

    def _resolve_odxlinks(self, odxlinks: OdxLinkDatabase) -> None:
        super()._resolve_odxlinks(odxlinks)
        for comparam in self.comparams:
            comparam._resolve_odxlinks(odxlinks)

    def _resolve_snrefs(self, diag_layer: "DiagLayer") -> None:
        super()._resolve_snrefs(diag_layer)
        for comparam in self.comparams:
            comparam._resolve_snrefs(diag_layer)
=======
# SPDX-License-Identifier: MIT
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union
from xml.etree import ElementTree

from .basecomparam import BaseComparam
from .nameditemlist import NamedItemList
from .odxlink import OdxDocFragment, OdxLinkDatabase, OdxLinkId
from .odxtypes import odxstr_to_bool
from .utils import dataclass_fields_asdict

if TYPE_CHECKING:
    from .diaglayer import DiagLayer

ComplexValue = List[Union[str, "ComplexValue"]]


def create_complex_value_from_et(et_element: ElementTree.Element) -> ComplexValue:
    result: ComplexValue = []
    for el in et_element:
        if el.tag == "SIMPLE-VALUE":
            result.append("" if el.text is None else el.text)
        else:
            result.append(create_complex_value_from_et(el))
    return result


@dataclass
class ComplexComparam(BaseComparam):
    subparams: NamedItemList[BaseComparam]
    physical_default_value: Optional[ComplexValue]
    allow_multiple_values_raw: Optional[bool]

    @property
    def allow_multiple_values(self) -> bool:
        return self.allow_multiple_values_raw is True

    @staticmethod
    def from_et(et_element: ElementTree.Element,
                doc_frags: List[OdxDocFragment]) -> "ComplexComparam":
        kwargs = dataclass_fields_asdict(BaseComparam.from_et(et_element, doc_frags))

        # to avoid a cyclic import, create_any_comparam_from_et cannot
        # be imported globally. TODO: figure out if this has
        # performance implications
        from .createanycomparam import create_any_comparam_from_et

        # extract the specifications of the sub-parameters and their
        # default values. Due to the quirky way this is defined by the
        # ODX specification, this is a *major* pain in the butt!
        subparams: NamedItemList[BaseComparam] = NamedItemList()
        elems = list(et_element)
        i = 0
        while i < len(elems):
            if elems[i].tag not in ("COMPARAM", "COMPLEX-COMPARAM"):
                i += 1
                continue

            subparam = create_any_comparam_from_et(elems[i], doc_frags)
            # the next element in the list *may* hold the physical
            # default value for the sub-parameter. if it is not the
            # correct tag, skip it! Note that the ODX specification
            # *only* allows to specify COMPLEX-PHYSICAL-DEFAULT-VALUE
            # tags here, even if the sub-parameter was a simple
            # parameter. This is probably a bug in the ODX
            # specification...
            if i + 1 < len(elems) and elems[i + 1].tag == "COMPLEX-PHYSICAL-DEFAULT-VALUE":
                subparam.physical_default_value = create_complex_value_from_et(elems[i + 1])
                i += 1

            subparams.append(subparam)
            i += 1

        allow_multiple_values_raw = odxstr_to_bool(et_element.get("ALLOW-MULTIPLE-VALUES"))

        return ComplexComparam(
            subparams=subparams,
            physical_default_value=[],
            allow_multiple_values_raw=allow_multiple_values_raw,
            **kwargs)

    def _build_odxlinks(self) -> Dict[OdxLinkId, Any]:
        odxlinks = super()._build_odxlinks()
        for subparam in self.subparams:
            odxlinks.update(subparam._build_odxlinks())
        return odxlinks

    def _resolve_odxlinks(self, odxlinks: OdxLinkDatabase) -> None:
        super()._resolve_odxlinks(odxlinks)
        for subparam in self.subparams:
            subparam._resolve_odxlinks(odxlinks)

    def _resolve_snrefs(self, diag_layer: "DiagLayer") -> None:
        super()._resolve_snrefs(diag_layer)
        for subparam in self.subparams:
            subparam._resolve_snrefs(diag_layer)
>>>>>>> 3e08420b53d6f9c3e3aa34ba078f1056425f441c
