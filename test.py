import os
import importlib.util
import inspect
from pathlib import Path

from telegram.ext import Application

def load_modules(app: Application):
    for py_file in Path("modules").glob("*.py"):
        module_name = py_file.stem
        if module_name.startswith('__'):
            continue
            
        spec = importlib.util.spec_from_file_location(module_name, py_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        functions = [name for name, obj in inspect.getmembers(module) 
                    if inspect.isfunction(obj) and not name.startswith('_')]
        
        print(f"Module: {module_name}")
        
        decorator_groups = {}
        
        for func_name in functions:
            func = getattr(module, func_name)
            
            # 데코레이터 이름 찾기
            if hasattr(func, '__wrapped__'):
                # 데코레이터가 적용된 함수
                decorator_name = func.__name__ if hasattr(func, '__name__') else 'unknown'
                # 실제 데코레이터 이름을 찾기 위해 원본 함수까지 추적
                original_func = func
                while hasattr(original_func, '__wrapped__'):
                    original_func = original_func.__wrapped__
                decorator_name = f"decorated_{original_func.__name__}"
            else:
                decorator_name = "no_decorator"
            
            if decorator_name not in decorator_groups:
                decorator_groups[decorator_name] = []
            decorator_groups[decorator_name].append(func_name)
        
        # 데코레이터별로 함수 실행
        for decorator_name, func_names in decorator_groups.items():
            print(f"\n[{decorator_name}]")
            print(f"Functions: {func_names}")
            
            for func_name in func_names:
                func = getattr(module, func_name)
                sig = inspect.signature(func)
                
                if len(sig.parameters) == 0:
                    if inspect.iscoroutinefunction(func):
                        import asyncio
                        result = asyncio.run(func())
                        print(f"{func_name}() -> {result}")
                    else:
                        result = func()
                        print(f"{func_name}() -> {result}")
                else:
                    try:
                        if inspect.iscoroutinefunction(func):
                            import asyncio
                            result = asyncio.run(func())
                            print(f"{func_name}() -> {result}")
                        else:
                            result = func()
                            print(f"{func_name}() -> {result}")
                    except:
                        print(f"{func_name}() -> needs parameters")
        
        print("="*50)

load_and_execute_modules()