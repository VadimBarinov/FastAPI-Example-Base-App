from typing import (
    Generator,
    Annotated,
)

from fastapi import (
    Request,
    HTTPException,
    status,
    Header,
)


class PathReaderDependency:
    def __init__(
            self,
            source: str,
    ) -> None:
        self.source = source
        self._request: Request | None = None

    def as_dependency(self, request: Request) -> Generator:
        self._request = request
        yield self
        self._request = None

    @property
    def path(self) -> str:
        if self._request is None:
            return ""
        return self._request.url.path

    def read(self, **kwargs: str) -> dict[str, str]:
        return {
            "source": self.source,
            "path": self.path,
            "kwargs": kwargs,
        }

path_reader = PathReaderDependency(source="abc/path/foo/bar")


class HeaderAccessDependency:
    def __init__(
            self,
            required_value: str,
    ) -> None:
        self.required_value = required_value
        pass

    def validate(self, token: str) -> str:
        if token != self.required_value:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is invalid"
            )
        return "Token data ....."


    def __call__(
            self,
            token: Annotated[
                str,
                Header(alias="x-access-token"),
            ]
    ) -> str:
        token_data = self.validate(token=token)
        return token_data

access_required = HeaderAccessDependency(required_value="foo-bar-fizz-buzz")
