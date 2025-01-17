<<<<<<< HEAD
# SPDX-License-Identifier: MIT
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional, cast
from xml.etree import ElementTree

from .element import IdentifiableElement
from .exceptions import odxraise, odxrequire
from .odxlink import OdxDocFragment, OdxLinkDatabase, OdxLinkId
from .utils import create_description_from_et

if TYPE_CHECKING:
    from .diaglayer import DiagLayer


class StandardizationLevel(Enum):
    STANDARD = "STANDARD"
    OEM_SPECIFIC = "OEM-SPECIFIC"
    OPTIONAL = "OPTIONAL"
    OEM_OPTIONAL = "OEM-OPTIONAL"


class Usage(Enum):
    ECU_SOFTWARE = "ECU-SOFTWARE"
    ECU_COMM = "ECU-COMM"
    APPLICATION = "APPLICATION"
    TESTER = "TESTER"


@dataclass
class BaseComparam(IdentifiableElement):
    param_class: str
    cptype: StandardizationLevel
    # Required in ODX 2.2, missing in ODX 2.0
    cpusage: Optional[Usage]
    display_level: Optional[int]

    def __init_from_et__(self, et_element: ElementTree.Element,
                         doc_frags: List[OdxDocFragment]) -> None:
        self.odx_id = odxrequire(OdxLinkId.from_et(et_element, doc_frags))
        self.short_name = odxrequire(et_element.findtext("SHORT-NAME"))
        self.long_name = et_element.findtext("LONG-NAME")
        self.description = create_description_from_et(et_element.find("DESC"))
        self.param_class = odxrequire(et_element.attrib.get("PARAM-CLASS"))

        cptype_str = odxrequire(et_element.attrib.get("CPTYPE"))
        try:
            self.cptype = StandardizationLevel(cptype_str)
        except ValueError:
            self.cptype = cast(StandardizationLevel, None)
            odxraise(f"Encountered unknown CPTYPE '{cptype_str}'")

        # Required in ODX 2.2, missing in ODX 2.0
        cpusage_str = et_element.attrib.get("CPUSAGE")
        if cpusage_str is not None:
            try:
                self.cpusage = Usage(cpusage_str)
            except ValueError:
                self.cpusage = None
                odxraise(f"Encountered unknown CPUSAGE '{cpusage_str}'")

        dl = et_element.attrib.get("DISPLAY_LEVEL")
        self.display_level = None if dl is None else int(dl)

    def _build_odxlinks(self) -> Dict[OdxLinkId, Any]:
        return {self.odx_id: self}

    def _resolve_odxlinks(self, odxlinks: OdxLinkDatabase) -> None:
        pass

    def _resolve_snrefs(self, diag_layer: "DiagLayer") -> None:
        pass
=======
# SPDX-License-Identifier: MIT
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional, cast
from xml.etree import ElementTree

from .element import IdentifiableElement
from .exceptions import odxraise, odxrequire
from .odxlink import OdxDocFragment, OdxLinkDatabase, OdxLinkId
from .utils import dataclass_fields_asdict

if TYPE_CHECKING:
    from .diaglayer import DiagLayer


class StandardizationLevel(Enum):
    STANDARD = "STANDARD"
    OEM_SPECIFIC = "OEM-SPECIFIC"
    OPTIONAL = "OPTIONAL"
    OEM_OPTIONAL = "OEM-OPTIONAL"


class Usage(Enum):
    ECU_SOFTWARE = "ECU-SOFTWARE"
    ECU_COMM = "ECU-COMM"
    APPLICATION = "APPLICATION"
    TESTER = "TESTER"


@dataclass
class BaseComparam(IdentifiableElement):
    param_class: str
    cptype: StandardizationLevel
    # Required in ODX 2.2, missing in ODX 2.0
    cpusage: Optional[Usage]
    display_level: Optional[int]

    @staticmethod
    def from_et(et_element: ElementTree.Element, doc_frags: List[OdxDocFragment]) -> "BaseComparam":
        kwargs = dataclass_fields_asdict(IdentifiableElement.from_et(et_element, doc_frags))

        param_class = odxrequire(et_element.attrib.get("PARAM-CLASS"))

        cptype_str = odxrequire(et_element.attrib.get("CPTYPE"))
        try:
            cptype = StandardizationLevel(cptype_str)
        except ValueError:
            cptype = cast(StandardizationLevel, None)
            odxraise(f"Encountered unknown CPTYPE '{cptype_str}'")

        dl = et_element.attrib.get("DISPLAY_LEVEL")
        display_level = None if dl is None else int(dl)

        # Required in ODX 2.2, missing in ODX 2.0
        cpusage_str = et_element.attrib.get("CPUSAGE")
        if cpusage_str is not None:
            try:
                cpusage = Usage(cpusage_str)
            except ValueError:
                cpusage = None
                odxraise(f"Encountered unknown CPUSAGE '{cpusage_str}'")

        return BaseComparam(
            param_class=param_class,
            cptype=cptype,
            display_level=display_level,
            cpusage=cpusage,
            **kwargs)

    def _build_odxlinks(self) -> Dict[OdxLinkId, Any]:
        return {self.odx_id: self}

    def _resolve_odxlinks(self, odxlinks: OdxLinkDatabase) -> None:
        pass

    def _resolve_snrefs(self, diag_layer: "DiagLayer") -> None:
        pass
>>>>>>> 3e08420b53d6f9c3e3aa34ba078f1056425f441c
