from FreeTAKServer.controllers.configuration.MainConfig import MainConfig

config = MainConfig.instance()


class ComponentRegistrationVariables:
    core_components_path = config.CoreComponentsPath
    core_components_import_root = config.CoreComponentsImportRoot
    external_components_path = config.ExternalComponentsPath
    external_components_import_root = config.ExternalComponentsImportRoot
