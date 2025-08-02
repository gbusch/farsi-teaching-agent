"""
Google Cloud Storage service for managing lesson data.
"""
import os
import streamlit as st
from typing import List, Optional
from google.cloud import storage
from config.settings import GCS_BUCKET_NAME, SENTENCES_PREFIX

class GCSService:
    """Service for interacting with Google Cloud Storage."""
    
    def __init__(self):
        self.client = storage.Client()
        self.bucket_name = GCS_BUCKET_NAME
    
    def get_bucket(self):
        """Get the GCS bucket."""
        return self.client.get_bucket(self.bucket_name)
    
    def load_sentences_for_unit(self, unit: str, sentences_dir: str = SENTENCES_PREFIX) -> Optional[List[str]]:
        """
        Load sentences for a specific unit from GCS.
        
        Args:
            unit: The unit name
            sentences_dir: Directory path in GCS (default: sentences/)
            
        Returns:
            List of sentences or None if error
        """
        try:
            bucket = self.get_bucket()
            blob = bucket.blob(os.path.join(sentences_dir, f"{unit}.txt"))
            content = blob.download_as_text()
            return [line.strip() for line in content.splitlines() if line.strip()]
        except Exception as e:
            st.error(f"Error reading '{unit}' from GCS: {e}")
            return None
    
    def list_unit_files(self, sentences_prefix: str = SENTENCES_PREFIX) -> List[str]:
        """
        List available unit files in GCS.
        
        Args:
            sentences_prefix: Prefix path in GCS bucket
            
        Returns:
            List of unit names (without .txt extension)
        """
        try:
            bucket = self.get_bucket()
            blobs = bucket.list_blobs(prefix=sentences_prefix)
            unit_files = []
            
            for blob in blobs:
                name = blob.name
                if name.endswith(".txt") and not name.endswith("/"):
                    base = name[len(sentences_prefix):]
                    if base:
                        unit_files.append(os.path.splitext(base)[0])
            
            return unit_files
        except Exception as e:
            st.error(f"Error listing files in '{sentences_prefix}' from GCS: {e}")
            return []
    
    def file_exists(self, file_path: str) -> bool:
        """
        Check if a file exists in GCS.
        
        Args:
            file_path: Path to the file in GCS
            
        Returns:
            True if file exists, False otherwise
        """
        try:
            bucket = self.get_bucket()
            blob = bucket.blob(file_path)
            return blob.exists()
        except Exception:
            return False