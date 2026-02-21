from dataclasses import dataclass
from typing import Optional

@dataclass(kw_only=True)
class Package:
    name: str
    version: str
    author: str = "unknown"
    description: str = "This is a package"
    runner: Optional[str] = None
    tags: Optional[list[str]] = None

    def __repr__(self) -> str:
        return f"'{self.runner} package '{self.name}' by {self.author} with version {self.version}"
    
    def __str__(self) -> str:
        return f"{self.author}/{self.name} :{self.runner}: {self.version}"
    
    def to_dict(self) -> dict:
        d = {
            "name": self.name,
            "version": self.version,
            "author": self.author,
            "description": self.description,
            "runner": self.runner,
            "tags": self.tags,
        }
        if self.runner:
            d["runner"] = self.runner
        if self.tags:
            d["tags"] = self.tags
        return d
    
    @classmethod
    def from_dict(cls, name: str, data: dict) -> 'Package':
        return Package(
            name=name,
            version=data.get("version", "Unknown"),
            author=data.get("author", "unknown"),
            description=data.get("description", "This is a package"),
            runner=data.get("runner", None),
            tags=data.get("tags", None)
        )

@dataclass(kw_only=True)
class RegistryPackage(Package):
    url: str
    sha256: Optional[str] = None

    def __repr__(self) -> str:
        return f"registry package '{self.name}' by {self.author} version {self.version} with url {self.url}"
    
    def to_package(self) -> Package:
        return Package(
            name=self.name,
            version=self.version,
            author=self.author,
            description=self.description,
            tags=self.tags,
            runner=self.runner
        )

    def to_dict(self) -> dict:
        base = super().to_dict()
        base["url"] = self.url
        if self.sha256:
            base["sha256"] = self.sha256
        return base

    @classmethod
    def from_dict(cls, name: str, data: dict) -> 'RegistryPackage':
        if "url" not in data or not data["url"]:
            raise ValueError("URL is required and cannot be empty")
        return RegistryPackage(
            name=name,
            version=data.get("version", "unknown"),
            author=data.get("author", "unknown"),
            description=data.get("description", "This is a package"),
            url=data["url"],
            sha256=data.get("sha256", None),
            runner=data.get("runner", None),
            tags=data.get("tags", None),
        )
