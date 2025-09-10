import asyncio
import uuid
from pathlib import Path

from app.core.interfaces.file_storage_interface import FileStorageInterface
from app.settings import FileStorageSettings


class LocalFileStorage(FileStorageInterface):
    """Local file storage implementation using filesystem."""

    def __init__(self, settings: FileStorageSettings):
        self.settings = settings
        self.base_path = settings.base_path
        self.base_url = settings.base_url.rstrip('/')
        self.allowed_extensions = settings.allowed_extensions
        self.max_file_size = settings.max_file_size
        
        # Ensure base directory exists
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _validate_file(self, content: bytes, filename: str) -> None:
        """Validate file content and extension."""
        # Check file size
        if len(content) > self.max_file_size:
            raise ValueError(f"File size exceeds maximum allowed size of {self.max_file_size} bytes")
        
        # Check file extension
        file_extension = Path(filename).suffix.lower()
        if file_extension not in self.allowed_extensions:
            raise ValueError(f"File extension '{file_extension}' is not allowed. Allowed extensions: {self.allowed_extensions}")

    def _generate_unique_filename(self, original_filename: str) -> str:
        """Generate a unique filename to avoid conflicts."""
        file_extension = Path(original_filename).suffix
        unique_id = str(uuid.uuid4())
        return f"{unique_id}{file_extension}"

    def _get_file_url(self, filename: str) -> str:
        """Generate full URL for the file."""
        return f"{self.base_url}/media/{filename}"

    async def save_file(self, content: bytes, filename: str) -> str:
        """Save a file and return its URL."""
        # Validate file
        self._validate_file(content, filename)
        
        # Generate unique filename
        unique_filename = self._generate_unique_filename(filename)
        file_path = self.base_path / unique_filename
        
        # Write file asynchronously
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._write_file_sync, file_path, content)
        
        # Return full URL
        return self._get_file_url(unique_filename)

    def _write_file_sync(self, file_path: Path, content: bytes) -> None:
        """Synchronous file write operation."""
        with open(file_path, "wb") as f:
            f.write(content)

    async def delete_file(self, filename: str) -> bool:
        """Delete a file by its filename."""
        file_path = self.base_path / filename
        
        if not file_path.exists():
            return False
        
        loop = asyncio.get_event_loop()
        try:
            await loop.run_in_executor(None, file_path.unlink)
            return True
        except OSError:
            return False

    async def file_exists(self, filename: str) -> bool:
        """Check if a file exists by its filename."""
        file_path = self.base_path / filename
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, file_path.exists)


def create_local_storage(settings: FileStorageSettings) -> LocalFileStorage:
    """Factory function to create LocalFileStorage instance."""
    return LocalFileStorage(settings)