from supabase import create_client
from backend.config import Config
import uuid

supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

CONTENT_TYPES = {
    'png': 'image/png',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'gif': 'image/gif',
    'webp': 'image/webp'
}

def upload_image(file_bytes, filename, content_type=None):
    try:
        ext = filename.rsplit('.', 1)[-1].lower()
        detected_type = CONTENT_TYPES.get(ext, 'image/jpeg')
        final_content_type = content_type or detected_type

        unique_filename = f"{uuid.uuid4()}_{filename}"
        
        supabase.storage.from_(Config.SUPABASE_BUCKET).upload(
            path=unique_filename,
            file=file_bytes,
            file_options={"content-type": final_content_type}
        )

        url = supabase.storage.from_(Config.SUPABASE_BUCKET).get_public_url(unique_filename)
        return {"url": url, "filename": unique_filename}
    except Exception as e:
        print(f"Upload error: {e}")
        return None
    
def delete_image(filename):
    """Delete image from Supabase Storage"""
    try:
        supabase.storage.from_(Config.SUPABASE_BUCKET).remove([filename])
        return True
    except Exception as e:
        print(f"Delete error: {e}")
        return False