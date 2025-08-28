from typing import Annotated

from fastapi import Header


def get_x_foo_bar(
        foobar: Annotated[str, Header(alias="x-foo-bar")] = "",
) -> str:
    return foobar


def get_header_dependency(
        header_name: str,
        default_value: str = "",
):

    def dependency(
            header: Annotated[str, Header(alias=header_name)] = default_value,
    ) -> str:
        pass

    return dependency