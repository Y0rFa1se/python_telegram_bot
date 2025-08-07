from pathlib import Path
import importlib.util
import inspect

from telegram.ext import Application, CommandHandler, CallbackQueryHandler


def load_modules(app: Application):
    for py_file in Path("modules").glob("*.py"):
        module_name = py_file.stem
        if module_name.startswith("__"):
            continue

        spec = importlib.util.spec_from_file_location(module_name, py_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        functions = [name for name, obj in inspect.getmembers(module) if inspect.isfunction(obj) and not name.startswith("_")]

        decorator_groups = {"command": [], "callback": []}

        for func_name in functions:
            func = getattr(module, func_name)

            if hasattr(func, "__wrapped__"):
                decorator_name = func.__name__ if hasattr(func, "__name__") else "unknown"
                original_func = func
                while hasattr(original_func, "__wrapped__"):
                    original_func = original_func.__wrapped__
                decorator_name = original_func.__name__
            else:
                raise ValueError(f"No decorator found for function {func_name} in module {module_name}")

            if decorator_name not in decorator_groups:
                raise ValueError(f"Decorator {decorator_name} not recognized in module {module_name}")

            decorator_groups[decorator_name].append(func_name)
            
        for decorator_name, func_names in decorator_groups.items():
            if decorator_name == "command":
                for func_name in func_names:
                    func = getattr(module, func_name)

                    app.add_handler(CommandHandler(func.command, func))

            elif decorator_name == "callback":
                for func_name in func_names:
                    func = getattr(module, func_name)

                    app.add_handler(CallbackQueryHandler(func))