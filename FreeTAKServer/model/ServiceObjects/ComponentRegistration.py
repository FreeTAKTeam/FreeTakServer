from .ComponentRegistrationVariables import ComponentRegistrationVariables as variables


class ComponentRegistration:
    """configuration for component registration"""

    def __init__(
        self,
        core_components_path=variables.core_components_path,
        core_components_import_root=variables.core_components_import_root,
        internal_components_path=variables.internal_components_path,
        internal_components_import_root=variables.internal_components_import_root,
        external_components_path=variables.external_components_path,
        external_components_import_root=variables.external_components_import_root,
    ):
        self.core_components_path = core_components_path
        self.core_components_import_root = core_components_import_root
        self.internal_components_path = internal_components_path
        self.internal_components_import_root= internal_components_import_root
        self.external_components_path = external_components_path
        self.external_components_import_root = external_components_import_root
