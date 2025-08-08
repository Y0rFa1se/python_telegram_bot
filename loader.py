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

        functions = []
        for name, obj in inspect.getmembers(module):
            if inspect.isfunction(obj) and not name.startswith("_"):
                functions.append(name)

        decorator_groups = {"command": [], "callback": []}

        for func_name in functions:
            func = getattr(module, func_name)

            if hasattr(func, "decorator"):
                decorator_name = func.decorator
            else:
                continue

            if decorator_name not in decorator_groups:
                continue

            decorator_groups[decorator_name].append(func_name)

        print(decorator_groups)
            
        for decorator_name, func_names in decorator_groups.items():
            if decorator_name == "command":
                for func_name in func_names:
                    func = getattr(module, func_name)

                    app.add_handler(CommandHandler(func.command, func))
                    print(f"Command handler for {func.command} added from module {module_name}")

            elif decorator_name == "callback":
                for func_name in func_names:
                    func = getattr(module, func_name)

                    app.add_handler(CallbackQueryHandler(func, pattern=f"^{func.callback_data}$"))
                    print(f"Callback handler for {func.callback_data} added from module {module_name}")