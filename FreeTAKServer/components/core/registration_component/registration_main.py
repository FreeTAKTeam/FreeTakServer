import pathlib
from digitalpy.routing.controller import Controller
from digitalpy.routing.request import Request
from digitalpy.routing.response import Response
from pathlib import PurePath
import importlib
import os
from .registration_constants import ROOT_COMPONENT_PATH


class Registration:
    def register_components(
        self,
        config,
        component_folder_path,
        import_root="FreeTAKServer.components.extended",
    ):
        if not os.path.isabs(component_folder_path):
            component_folder_path = str(
                pathlib.PurePath(ROOT_COMPONENT_PATH, component_folder_path)
            )
        components = os.scandir(component_folder_path)
        for component in components:
            try:
                facade_path = PurePath(component.path, component.name + "_facade.py")
                if os.path.exists(facade_path):
                    component_name = component.name.replace("_component", "")
                    component_facade = getattr(
                        importlib.import_module(
                            f"{import_root}.{component.name}.{component_name}_facade"
                        ),
                        f"{''.join([name.capitalize() if name[0].isupper()==False else name for name in component_name.split('_')])}",
                    )
                    component_facade(None, None, None, None).register(config)
            except Exception as e:
                print(f"failed to register component: {component}, with error: {e}")
