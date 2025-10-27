#!/usr/bin/env python3
"""
SharePoint integration for Policy Chat Bot
"""

import os
import asyncio
from typing import List, Dict, Any
from datetime import datetime, timedelta
import requests
from pathlib import Path

# Microsoft Graph API integration
from msal import ConfidentialClientApplication
import msal

class SharePointIntegration:
    def __init__(self, config):
        self.config = config
        self.app = ConfidentialClientApplication(
            config.CLIENT_ID,
            authority=f"https://login.microsoftonline.com/{config.TENANT_ID}",
            client_credential=config.CLIENT_SECRET
        )
        self.access_token = None
        self.graph_url = "https://graph.microsoft.com/v1.0"
    
    def get_access_token(self):
        """Get access token for Microsoft Graph API"""
        try:
            result = self.app.acquire_token_for_client(
                scopes=["https://graph.microsoft.com/.default"]
            )
            
            if "access_token" in result:
                self.access_token = result["access_token"]
                return True
            else:
                print(f"❌ Token acquisition failed: {result.get('error_description')}")
                return False
                
        except Exception as e:
            print(f"❌ Error getting access token: {str(e)}")
            return False
    
    def get_sharepoint_sites(self):
        """Get all SharePoint sites"""
        if not self.access_token:
            if not self.get_access_token():
                return []
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(
                f"{self.graph_url}/sites",
                headers=headers
            )
            
            if response.status_code == 200:
                sites = response.json().get("value", [])
                return sites
            else:
                print(f"❌ Error getting sites: {response.text}")
                return []
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return []
    
    def get_documents_from_library(self, site_id: str, library_name: str):
        """Get documents from a specific SharePoint library"""
        if not self.access_token:
            if not self.get_access_token():
                return []
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        try:
            # Get documents from the library
            url = f"{self.graph_url}/sites/{site_id}/drives"
            response = requests.get(url, headers=headers)
            
            if response.status_code != 200:
                print(f"❌ Error getting drives: {response.text}")
                return []
            
            drives = response.json().get("value", [])
            target_drive = None
            
            for drive in drives:
                if drive["name"] == library_name:
                    target_drive = drive
                    break
            
            if not target_drive:
                print(f"❌ Drive '{library_name}' not found")
                return []
            
            # Get files from the drive
            drive_id = target_drive["id"]
            files_url = f"{self.graph_url}/drives/{drive_id}/root/children"
            
            files_response = requests.get(files_url, headers=headers)
            
            if files_response.status_code == 200:
                files = files_response.json().get("value", [])
                # Filter for supported document types
                supported_extensions = ['.pdf', '.docx', '.txt', '.md']
                documents = [
                    file for file in files 
                    if file.get("file", {}).get("mimeType") and
                    any(file["name"].lower().endswith(ext) for ext in supported_extensions)
                ]
                return documents
            else:
                print(f"❌ Error getting files: {files_response.text}")
                return []
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return []
    
    def download_document(self, site_id: str, drive_id: str, file_id: str, file_name: str):
        """Download a document from SharePoint"""
        if not self.access_token:
            if not self.get_access_token():
                return None
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/octet-stream"
        }
        
        try:
            # Download file content
            url = f"{self.graph_url}/drives/{drive_id}/items/{file_id}/content"
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                # Save to temporary location
                temp_path = f"/tmp/{file_name}"
                with open(temp_path, 'wb') as f:
                    f.write(response.content)
                return temp_path
            else:
                print(f"❌ Error downloading {file_name}: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error downloading {file_name}: {str(e)}")
            return None
    
    def sync_sharepoint_documents(self, site_id: str, library_name: str, vector_store):
        """Sync documents from SharePoint to vector store"""
        print(f"🔄 Syncing documents from SharePoint library: {library_name}")
        
        # Get documents from SharePoint
        documents = self.get_documents_from_library(site_id, library_name)
        
        if not documents:
            print("❌ No documents found in SharePoint library")
            return
        
        print(f"📁 Found {len(documents)} documents in SharePoint")
        
        # Process each document
        from document_processor import DocumentProcessor
        processor = DocumentProcessor()
        
        synced_count = 0
        for doc in documents:
            try:
                file_name = doc["name"]
                file_id = doc["id"]
                drive_id = doc["parentReference"]["driveId"]
                
                print(f"🔄 Processing: {file_name}")
                
                # Download document
                temp_path = self.download_document(site_id, drive_id, file_id, file_name)
                
                if temp_path:
                    # Process document
                    processed_docs = processor.process_document(temp_path)
                    
                    # Add metadata about SharePoint source
                    for processed_doc in processed_docs:
                        processed_doc.metadata.update({
                            "sharepoint_source": True,
                            "sharepoint_file_id": file_id,
                            "sharepoint_drive_id": drive_id,
                            "sharepoint_site_id": site_id,
                            "last_synced": datetime.now().isoformat()
                        })
                    
                    # Add to vector store
                    success = vector_store.add_documents(processed_docs)
                    
                    if success:
                        synced_count += len(processed_docs)
                        print(f"✅ Synced {len(processed_docs)} chunks from {file_name}")
                    else:
                        print(f"❌ Failed to sync {file_name}")
                    
                    # Clean up temp file
                    os.remove(temp_path)
                else:
                    print(f"❌ Failed to download {file_name}")
                    
            except Exception as e:
                print(f"❌ Error processing {doc.get('name', 'unknown')}: {str(e)}")
        
        print(f"🎉 Sync completed: {synced_count} total chunks synced")

class SharePointConfig:
    def __init__(self):
        # SharePoint/Office 365 configuration
        self.CLIENT_ID = os.getenv("SHAREPOINT_CLIENT_ID")
        self.CLIENT_SECRET = os.getenv("SHAREPOINT_CLIENT_SECRET")
        self.TENANT_ID = os.getenv("SHAREPOINT_TENANT_ID")
        
        # SharePoint site configuration
        self.POLICY_SITE_ID = os.getenv("SHAREPOINT_POLICY_SITE_ID")
        self.POLICY_LIBRARY_NAME = os.getenv("SHAREPOINT_POLICY_LIBRARY_NAME", "Documents")
        
        # Sync settings
        self.SYNC_INTERVAL_HOURS = int(os.getenv("SHAREPOINT_SYNC_INTERVAL", "24"))
        self.AUTO_SYNC = os.getenv("SHAREPOINT_AUTO_SYNC", "false").lower() == "true"

def setup_sharepoint_sync():
    """Set up SharePoint sync for production"""
    
    config = SharePointConfig()
    
    if not all([config.CLIENT_ID, config.CLIENT_SECRET, config.TENANT_ID]):
        print("❌ SharePoint configuration incomplete")
        print("Required environment variables:")
        print("- SHAREPOINT_CLIENT_ID")
        print("- SHAREPOINT_CLIENT_SECRET") 
        print("- SHAREPOINT_TENANT_ID")
        print("- SHAREPOINT_POLICY_SITE_ID")
        return None
    
    # Initialize SharePoint integration
    sharepoint = SharePointIntegration(config)
    
    # Test connection
    if sharepoint.get_access_token():
        print("✅ SharePoint connection successful")
        return sharepoint
    else:
        print("❌ SharePoint connection failed")
        return None

if __name__ == "__main__":
    # Test SharePoint integration
    sharepoint = setup_sharepoint_sync()
    
    if sharepoint:
        # List available sites
        sites = sharepoint.get_sharepoint_sites()
        print(f"📁 Available SharePoint sites: {len(sites)}")
        
        for site in sites[:5]:  # Show first 5 sites
            print(f"  - {site['displayName']} ({site['id']})")



