"""
Project Manager Module
======================

Handles saving, loading, and managing ClickSUMO simulation projects.

Features:
- Save complete simulation projects
- Load previous projects
- Export/Import project files
- Project metadata and versioning
- Auto-save functionality

Author: Mahbub Hassan
Copyright © 2026 Mahbub Hassan
"""

import json
import streamlit as st
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import zipfile
import io


class ProjectManager:
    """Manages saving and loading of ClickSUMO projects."""

    def __init__(self, projects_dir: str = "saved_projects"):
        """
        Initialize project manager.

        Args:
            projects_dir: Directory to store saved projects
        """
        self.projects_dir = Path(projects_dir)
        self.projects_dir.mkdir(exist_ok=True)

    def save_project(self, project_name: str, description: str = "") -> bool:
        """
        Save current session state as a project.

        Args:
            project_name: Name for the project
            description: Optional project description

        Returns:
            True if successful, False otherwise
        """
        try:
            # Create project data
            project_data = {
                'metadata': {
                    'name': project_name,
                    'description': description,
                    'created': datetime.now().isoformat(),
                    'version': '1.0',
                    'app_version': '8.0 (NEBULA AI)'
                },
                'network': st.session_state.get('network'),
                'routes': st.session_state.get('routes'),
                'tls_programs': st.session_state.get('tls_programs', {}),
                'generated_files': st.session_state.get('generated_files', []),
                'config_data': {
                    'net_file': st.session_state.get('net_file'),
                    'route_file': st.session_state.get('route_file'),
                    'add_file': st.session_state.get('add_file'),
                }
            }

            # Save to file
            project_file = self.projects_dir / f"{project_name}.json"
            with open(project_file, 'w') as f:
                json.dump(project_data, f, indent=2)

            return True

        except Exception as e:
            st.error(f"Error saving project: {e}")
            return False

    def load_project(self, project_name: str) -> bool:
        """
        Load a saved project into session state.

        Args:
            project_name: Name of the project to load

        Returns:
            True if successful, False otherwise
        """
        try:
            project_file = self.projects_dir / f"{project_name}.json"

            if not project_file.exists():
                st.error(f"Project '{project_name}' not found")
                return False

            # Load project data
            with open(project_file, 'r') as f:
                project_data = json.load(f)

            # Restore session state
            st.session_state.network = project_data.get('network')
            st.session_state.routes = project_data.get('routes')
            st.session_state.tls_programs = project_data.get('tls_programs', {})
            st.session_state.generated_files = project_data.get('generated_files', [])

            # Restore config data
            config = project_data.get('config_data', {})
            st.session_state.net_file = config.get('net_file')
            st.session_state.route_file = config.get('route_file')
            st.session_state.add_file = config.get('add_file')

            return True

        except Exception as e:
            st.error(f"Error loading project: {e}")
            return False

    def delete_project(self, project_name: str) -> bool:
        """
        Delete a saved project.

        Args:
            project_name: Name of the project to delete

        Returns:
            True if successful, False otherwise
        """
        try:
            project_file = self.projects_dir / f"{project_name}.json"

            if project_file.exists():
                project_file.unlink()
                return True
            return False

        except Exception as e:
            st.error(f"Error deleting project: {e}")
            return False

    def list_projects(self) -> List[Dict]:
        """
        Get list of all saved projects with metadata.

        Returns:
            List of project information dictionaries
        """
        projects = []

        for project_file in self.projects_dir.glob("*.json"):
            try:
                with open(project_file, 'r') as f:
                    data = json.load(f)

                metadata = data.get('metadata', {})
                projects.append({
                    'name': metadata.get('name', project_file.stem),
                    'description': metadata.get('description', ''),
                    'created': metadata.get('created', 'Unknown'),
                    'version': metadata.get('version', '1.0'),
                    'has_network': bool(data.get('network')),
                    'has_routes': bool(data.get('routes')),
                    'file_path': str(project_file)
                })

            except Exception as e:
                # Skip corrupted files
                continue

        # Sort by creation date (newest first)
        projects.sort(key=lambda x: x['created'], reverse=True)
        return projects

    def export_project(self, project_name: str) -> Optional[bytes]:
        """
        Export a project as a ZIP file.

        Args:
            project_name: Name of the project to export

        Returns:
            ZIP file as bytes, or None if error
        """
        try:
            project_file = self.projects_dir / f"{project_name}.json"

            if not project_file.exists():
                return None

            # Create ZIP in memory
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                # Add project JSON
                zip_file.write(project_file, f"{project_name}.json")

                # Add README
                readme = f"""ClickSUMO Project Export
========================

Project Name: {project_name}
Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This ZIP contains your ClickSUMO simulation project.

To import:
1. Open ClickSUMO
2. Go to any page
3. Click "📁 Manage Projects" in sidebar
4. Use "Import Project" feature
5. Upload this ZIP file

Version: 8.0 (NEBULA AI)
© 2026 Mahbub Hassan
"""
                zip_file.writestr("README.txt", readme)

            zip_buffer.seek(0)
            return zip_buffer.getvalue()

        except Exception as e:
            st.error(f"Error exporting project: {e}")
            return None

    def import_project(self, uploaded_file) -> bool:
        """
        Import a project from uploaded ZIP file.

        Args:
            uploaded_file: Streamlit UploadedFile object

        Returns:
            True if successful, False otherwise
        """
        try:
            # Extract ZIP
            with zipfile.ZipFile(uploaded_file, 'r') as zip_file:
                # Find JSON file
                json_files = [f for f in zip_file.namelist() if f.endswith('.json')]

                if not json_files:
                    st.error("No project file found in ZIP")
                    return False

                # Extract and save project
                json_content = zip_file.read(json_files[0])
                project_data = json.loads(json_content)

                # Get project name from metadata
                project_name = project_data.get('metadata', {}).get('name', 'imported_project')

                # Save to projects directory
                project_file = self.projects_dir / f"{project_name}.json"
                with open(project_file, 'wb') as f:
                    f.write(json_content)

                return True

        except Exception as e:
            st.error(f"Error importing project: {e}")
            return False

    def get_project_info(self, project_name: str) -> Optional[Dict]:
        """
        Get detailed information about a project.

        Args:
            project_name: Name of the project

        Returns:
            Project information dictionary, or None if not found
        """
        try:
            project_file = self.projects_dir / f"{project_name}.json"

            if not project_file.exists():
                return None

            with open(project_file, 'r') as f:
                data = json.load(f)

            metadata = data.get('metadata', {})

            # Count components
            network_components = 0
            if data.get('network'):
                network_data = data['network']
                if isinstance(network_data, dict):
                    network_components = (
                        len(network_data.get('nodes', [])) +
                        len(network_data.get('edges', []))
                    )

            route_count = 0
            if data.get('routes'):
                route_count = len(data['routes'].get('vehicles', []))

            return {
                'name': metadata.get('name', project_name),
                'description': metadata.get('description', ''),
                'created': metadata.get('created', 'Unknown'),
                'version': metadata.get('version', '1.0'),
                'app_version': metadata.get('app_version', 'Unknown'),
                'network_components': network_components,
                'route_count': route_count,
                'has_network': bool(data.get('network')),
                'has_routes': bool(data.get('routes')),
                'has_tls': bool(data.get('tls_programs')),
                'file_size': project_file.stat().st_size,
                'file_path': str(project_file)
            }

        except Exception as e:
            return None
