import os
from werkzeug.utils import secure_filename
import uuid
 
UPLOADS_DIR = "uploads"
 
def save_file(file, folder):
    """Saves an uploaded file to a specific folder and returns the relative path."""
    if not file:
        return None
 
    # Create absolute path for saving
    target_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), UPLOADS_DIR, folder)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
 
    # Generate a unique filename to avoid collisions
    original_filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4().hex}_{original_filename}"
    file_path = os.path.join(target_dir, unique_filename)
 
    file.save(file_path)
    
    # Return path relative to backend root
    return os.path.join(UPLOADS_DIR, folder, unique_filename)
