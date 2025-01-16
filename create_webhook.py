def copy_file(src: str, dest: str):
    with open(src, "r") as src_file:
        with open(dest, "w") as dest_file:
            dest_file.write(src_file.read())


def compute_class_name(webhook_name: str):
    return webhook_name.replace("_", " ").title().replace(" ", "")


def replace_in_handler_file(
    file_path: str,
    old_class_name: str,
    new_class_name: str,
    old_file_name: str,
    new_file_name: str,
):
    with open(file_path, "r") as file:
        filedata = file.read()
        filedata = filedata.replace(old_class_name, new_class_name)
        filedata = filedata.replace(old_file_name, new_file_name)

    with open(file_path, "w") as file:
        file.write(filedata)


def update_init_file(init_file_path: str, class_name: str, handler_file_name: str):

    with open(init_file_path, "r") as file:
        filedata = file.read()
        lines = filedata.split("\n")

        import_line = f"from .{handler_file_name} import {class_name}"
        all_line = f'    "{class_name}",'

        # fin the index of the last import line
        import_index = -1
        for i, line in enumerate(lines):
            if line.startswith("from ."):
                import_index = i

        # find the index of the last __all__ line
        all_index = -1
        for i, line in enumerate(lines):
            if line.startswith(']'):
                all_index = i

        # insert the new import line
        lines.insert(import_index + 1, import_line)
        # insert the new __all__ line
        lines.insert(all_index + 1, all_line)
    with open(init_file_path, "w") as file:
        file.write("\n".join(lines))

def update_factory_file(factory_file_path: str, class_name: str, handler_file_name: str):
    """
    from typing import Dict, Type

from handlers import (
    HandlerExample,
)
from utils.base import HandlerBase


class HandlerFactory:
    _handlers: Dict[str, Type[HandlerBase]] = {
        "handler_example": HandlerExample,
    }

    def __call__(self, tag: str):
        handler_class = self._handlers.get(tag)
        if not handler_class:
            raise ValueError(f"Unknown handler tag: {tag}")
        return handler_class()

    """

    with open(factory_file_path, "r") as file:
        filedata = file.read()
        lines = filedata.split("\n")

        import_line = class_name
        handlers_line = f'"{handler_file_name}": {class_name},'

        # fin the index of the last import line
        import_index = -1
        for i, line in enumerate(lines):
            if line.strip().startswith(")"):
                # get the number of tabs in the previous line
                import_tabs = len(lines[i - 1]) - len(lines[i - 1].lstrip())
                import_index = i

        # find the index of the last dict line
        handlers_index = -1
        for i, line in enumerate(lines):
            if line.strip().startswith("}"):
                # get the number of tabs in the previous line
                handlers_tabs = len(lines[i - 1]) - len(lines[i - 1].lstrip())
                handlers_index = i

        # insert the new import line
        lines.insert(import_index, import_tabs * " " + import_line)
        # insert the new __all__ line
        lines.insert(handlers_index + 1, handlers_tabs * " " + handlers_line)

    with open(factory_file_path, "w") as file:
        file.write("\n".join(lines))

def create_webhook(webhook_name: str):
    ROOT = "modules/resources/webhook_function_code/"
    TEMPLATE_PATH = ROOT + "handlers/handler_example.py"
    NEW_HANDLER_PATH = ROOT + f"handlers/{webhook_name}.py"
    OLD_CLASS_NAME = "HandlerExample"
    NEW_CLASS_NAME = compute_class_name(webhook_name)
    INIT_FILE_PATH = ROOT + "handlers/__init__.py"
    FACTORY_FILE_PATH = ROOT + "utils/factory.py"

    copy_file(
        src=TEMPLATE_PATH,
        dest=NEW_HANDLER_PATH,
    )
    print("Template file copied successfully!")

    replace_in_handler_file(
        file_path=NEW_HANDLER_PATH,
        old_class_name=OLD_CLASS_NAME,
        new_class_name=NEW_CLASS_NAME,
        old_file_name="handler_example",
        new_file_name=webhook_name,
    )
    print("Class name replaced successfully in the created handler file!")

    update_init_file(
        init_file_path=INIT_FILE_PATH,
        class_name=NEW_CLASS_NAME,
        handler_file_name=webhook_name,
    )
    print("Class name added to the __init__.py file successfully!")

    update_factory_file(
        factory_file_path=FACTORY_FILE_PATH,
        class_name=NEW_CLASS_NAME,
        handler_file_name=webhook_name,
    )
    print("Class name added to the factory.py file successfully!")


if __name__ == "__main__":
    # read the arguments from the command line
    import sys
    webhook_name = sys.argv[1]
    create_webhook(webhook_name)
