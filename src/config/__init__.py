"""
Configuration package for Mist API Office Automation Project.

This package contains configuration management modules for various components
of the system.
"""

from .auth_config import get_mist_config, create_env_template

__all__ = ['get_mist_config', 'create_env_template']
