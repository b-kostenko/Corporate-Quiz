from abc import ABC, abstractmethod


class FileStorageInterface(ABC):
    """Interface for file storage operations."""

    @abstractmethod
    async def save_file(self, content: bytes, filename: str) -> str:
        """Saves a file and returns its URL or path."""
        pass

    @abstractmethod
    async def delete_file(self, filename: str) -> bool:
        """Deletes a file by its filename. Returns True if successful."""
        pass

    @abstractmethod
    async def file_exists(self, filename: str) -> bool:
        """Checks if a file exists by its filename."""
        pass
