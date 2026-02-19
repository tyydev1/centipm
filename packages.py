from dataclasses import dataclass

@dataclass(kw_only=True)
class Package:
    name: str
    version: str
    description: str = "This is a package"

    def __str__(self) -> str:
        return f"package '{self.name}' with version {self.version}"
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Package':
        return Package(
            name=data.get("name", "Unknown"),
            version=data.get("version", "Unknown"),
            description=data.get("description", "This is a package")
        )

@dataclass(kw_only=True)
class RegistryPackage(Package):
    url: str

    def __str__(self) -> str:
        return f"registry package '{self.name}' version {self.version} with url {self.url}"
    
    def to_dict(self) -> dict:
        base = super().to_dict()
        base["url"] = self.url
        return base

    @classmethod
    def from_dict(cls, data: dict) -> 'RegistryPackage':
        if "url" not in data or not data["url"]:
            raise ValueError("URL is required and cannot be empty")
        return RegistryPackage(
            name=data.get("name", "Unknown"),
            version=data.get("version", "Unknown"),
            description=data.get("description", "This is a package"),
            url=data["url"]
        )

def main():
    dummy: Package = RegistryPackage(
        name="hello",
        version="1.0.2-dev",
        url="https://example.com/api"
    )
    print(dummy)
    
if __name__ == "__main__":
    main()