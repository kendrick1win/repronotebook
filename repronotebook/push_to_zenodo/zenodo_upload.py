# repronotebook/push_to_zenodo/zenodo_upload.py

import os
import requests
import json
from pathlib import Path
from rich import print
from typing import Optional, Dict, Any

class ZenodoUploader:
    def __init__(self, access_token: Optional[str] = None, sandbox: bool = False):
        """
        Initialize Zenodo uploader with API token.
        
        Args:
            access_token: Zenodo API token. If None, reads from ZENODO_TOKEN env var
            sandbox: Use Zenodo sandbox for testing (default: False)
        """
        self.access_token = access_token or os.getenv("ZENODO_TOKEN")
        if not self.access_token:
            raise ValueError("Zenodo API token required. Set ZENODO_TOKEN environment variable or pass access_token parameter.")
        
        self.base_url = "https://sandbox.zenodo.org/api" if sandbox else "https://zenodo.org/api"
        self.params = {"access_token": self.access_token}
    
    def create_deposition(self, metadata: Dict[str, Any]) -> str:
        """
        Create a new deposition on Zenodo.
        
        Args:
            metadata: Zenodo metadata dictionary
            
        Returns:
            Deposition ID
        """
        print("[bold]🚀 Creating new Zenodo deposition...[/]")
        
        response = requests.post(
            f"{self.base_url}/deposit/depositions",
            params=self.params,
            json={"metadata": metadata},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code != 201:
            raise Exception(f"Failed to create deposition: {response.status_code} - {response.text}")
        
        deposition_data = response.json()
        deposition_id = deposition_data["id"]
        
        print(f"[green]✅ Deposition created with ID: {deposition_id}[/]")
        return str(deposition_id)
    
    def upload_file(self, deposition_id: str, file_path: Path) -> bool:
        """
        Upload a file to an existing Zenodo deposition.
        
        Args:
            deposition_id: The deposition ID
            file_path: Path to file to upload
            
        Returns:
            True if successful
        """
        print(f"[bold]📤 Uploading file: {file_path.name}...[/]")
        
        # Get bucket URL for file upload
        deposition_response = requests.get(
            f"{self.base_url}/deposit/depositions/{deposition_id}",
            params=self.params
        )
        
        if deposition_response.status_code != 200:
            raise Exception(f"Failed to get deposition info: {deposition_response.status_code}")
        
        bucket_url = deposition_response.json()["links"]["bucket"]
        
        # Upload file using PUT to bucket
        with open(file_path, 'rb') as file:
            upload_response = requests.put(
                f"{bucket_url}/{file_path.name}",
                data=file,
                params=self.params
            )
        
        if upload_response.status_code not in [200, 201]:
            raise Exception(f"Failed to upload file: {upload_response.status_code} - {upload_response.text}")
        
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        print(f"[green]✅ Uploaded {file_path.name} ({file_size_mb:.1f} MB)[/]")
        return True
    
    def publish_deposition(self, deposition_id: str) -> str:
        """
        Publish a deposition to make it publicly available.
        
        Args:
            deposition_id: The deposition ID
            
        Returns:
            DOI of published record
        """
        print("[bold]🔓 Publishing deposition...[/]")
        
        response = requests.post(
            f"{self.base_url}/deposit/depositions/{deposition_id}/actions/publish",
            params=self.params
        )
        
        if response.status_code != 202:
            raise Exception(f"Failed to publish deposition: {response.status_code} - {response.text}")
        
        published_data = response.json()
        doi = published_data["doi"]
        
        print(f"[green]✅ Published successfully! DOI: {doi}[/]")
        return doi


def upload_ro_crate_to_zenodo(
    crate_zip_path: Path, 
    zenodo_metadata: Dict[str, Any],
    access_token: Optional[str] = None,
    sandbox: bool = False,
    publish: bool = False
) -> Dict[str, str]:
    """
    Upload an RO-Crate ZIP file to Zenodo.
    
    Args:
        crate_zip_path: Path to the RO-Crate ZIP file
        zenodo_metadata: Zenodo metadata dictionary
        access_token: Zenodo API token (optional, reads from env)
        sandbox: Use sandbox environment (default: False)
        publish: Automatically publish after upload (default: False)
        
    Returns:
        Dictionary with deposition_id and optional DOI
    """
    uploader = ZenodoUploader(access_token=access_token, sandbox=sandbox)
    
    # Determine the correct base web URL
    web_base_url = "https://sandbox.zenodo.org" if sandbox else "https://zenodo.org"
    
    try:
        # Create deposition
        deposition_id = uploader.create_deposition(zenodo_metadata)
        
        # Upload ZIP file
        uploader.upload_file(deposition_id, crate_zip_path)
        
        result = {"deposition_id": deposition_id}
        
        # Publish if requested
        if publish:
            doi = uploader.publish_deposition(deposition_id)
            result["doi"] = doi
            print(f"[bold green]🎉 RO-Crate successfully uploaded and published![/]")
            print(f"[bold]📄 Access your dataset at: {web_base_url}/record/{deposition_id}[/]")
        else:
            print(f"[bold yellow]⚠️ RO-Crate uploaded but not published. Visit Zenodo to review and publish.[/]")
            print(f"[bold]📄 Review at: {web_base_url}/deposit/{deposition_id}[/]")
        
        return result
        
    except Exception as e:
        print(f"[red]❌ Zenodo upload failed: {str(e)}[/]")
        raise