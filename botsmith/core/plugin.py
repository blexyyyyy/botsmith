import importlib
import pkgutil
import sys
from pathlib import Path
from typing import Dict, Type, Any

class BasePlugin:
    """
    Base interface for BotSmith plugins.
    """
    name: str = "unnamed_plugin"
    version: str = "0.0.1"

    def register(self, registry: Any):
        """
        Register plugin capabilities (agents, workflows, etc.).
        """
        pass

class PluginManager:
    """
    Discovers and loads plugins.
    """
    def __init__(self, plugin_dir: str = "plugins"):
        self.plugin_dir = plugin_dir
        self.plugins: Dict[str, BasePlugin] = {}

    def load_plugins(self):
        """
        Load plugins from the plugin directory and installed packages.
        """
        # 1. Load from local 'plugins' dir if exists
        local_plugins = Path(self.plugin_dir)
        if local_plugins.exists():
            sys.path.append(str(local_plugins.resolve()))
            for _, name, _ in pkgutil.iter_modules([str(local_plugins)]):
                self._load_module(name)

        # 2. Could also load entry points here (e.g. 'botsmith.plugins')
        
    def _load_module(self, name: str):
        try:
            module = importlib.import_module(name)
            if hasattr(module, "Plugin") and issubclass(module.Plugin, BasePlugin):
                plugin = module.Plugin()
                self.plugins[plugin.name] = plugin
                print(f"[PluginManager] Loaded plugin: {plugin.name} v{plugin.version}")
                # plugin.register(...)
        except Exception as e:
            print(f"[PluginManager] Failed to load plugin {name}: {e}")
