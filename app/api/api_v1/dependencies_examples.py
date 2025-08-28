from fastapi import (
    APIRouter,
    Depends,
    Header
)
from typing import Annotated
from utils.helpers import GreatHelper

from .dependencies.func_dep import (
    get_x_foo_bar,
    get_header_dependency,
)
from .dependencies.cls_deps import (
    PathReaderDependency,
    access_required,

)

router = APIRouter(
    tags=["Dependencies examples",],
)


@router.get("/single-direct-dependency", response_model=dict)
def single_direct_dependency(
        foobar: Annotated[str, Header(alias="x-foo-bar")],
):
    return {
        "foobar": foobar,
        "message": "single direct dependency foobar",
    }


@router.get("/single-via-func", response_model=dict)
def single_via_func(
        foobar: Annotated[str, Depends(get_x_foo_bar)],
):
    return {
        "x-foo-bar": foobar,
        "message": "single via-func dependency",
    }


@router.get("/multi-direct-and-via-func", response_model=dict)
def multi_direct_and_via_func(
        fizzbuzz: Annotated[str, Header(alias="x-fizz-buzz")],
        foobar: Annotated[str, Depends(get_x_foo_bar)],
):
    return {
        "x-fizz-buzz": fizzbuzz,
        "x-foo-bar": foobar,
        "message": "multi-direct and via-func dependency",
    }


@router.get("/multi-indirect", response_model=dict)
def multi_indirect_dependencies(
        foobar: Annotated[
            str,
            Depends(get_header_dependency("x-foo-bar")),
        ],
        fizzbuzz: Annotated[
            str,
            Depends(
                get_header_dependency(
                    header_name="x-fizz-buzz",
                    default_value="FizzBuzz"
                )
            )
        ]
):
    return {
        "x-fizz-buzz": fizzbuzz,
        "x-foo-bar": foobar,
        "message": "multi-indirect dependency",
    }

@router.get("/top-level-helper-creation", response_model=dict)
def top_level_helper_creation(
        helper_name: Annotated[
            str,
            Depends(
                get_header_dependency(
                    header_name="x-helper-name",
                    default_value="HelperOne"
                )
            )
        ],
        helper_default: Annotated[
            str,
            Depends(
                get_header_dependency(
                    header_name="x-helper-default-value",
                )
            )
        ]
):
    helper = GreatHelper(
        name=helper_name,
        default=helper_default
    )

    return {
        "helper": helper.as_dict(),
        "message": "top level helper creation",
    }


@router.get("/path-reader-dependency-from-method", response_model=dict)
def path_reader_dependency(
        reader: Annotated[
            PathReaderDependency,
            Depends(PathReaderDependency.as_dependency)
        ]
):
    return {
        "reader": reader.read(foo="bar"),
        "message": "path-reader-dependency-from-method",
    }


@router.get("/direct-cls-dependency", response_model=dict)
def direct_cls_dependency(
        token_data: Annotated[
            str,
            Depends(access_required),
        ],
):
    return {
        "token_data": token_data,
        "message": "direct-cls-dependency",
    }