import pathlib
from digitalpy.routing.controller import Controller
from digitalpy.routing.request import Request
from digitalpy.routing.response import Response
from pathlib import PurePath
import importlib
import os


class Registration:
    def register_components(
        self,
        config,
        component_folder_path=pathlib.Path(
            pathlib.Path(__file__).parent.parent.absolute(), "extended"
        ),
        import_root="FreeTAKServer.components.extended",
    ):
        components = os.scandir(component_folder_path)
        for component in components:
            facade_path = PurePath(component.path, component.name + "_facade.py")
            if os.path.exists(facade_path):
                component_name = component.name.replace("_component", "")
                component_facade = getattr(
                    importlib.import_module(
                        f"{import_root}.{component.name}.{component_name}_facade"
                    ),
                    f"{component_name.capitalize()}Facade",
                )
                component_facade().register(config)
