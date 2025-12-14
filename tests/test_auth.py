"""Tests for authentication system."""

import os
from auth import authenticate_dev, DEV_USERNAME, DEV_PASSWORD
from auth.manager import AuthManager


def test_dev_login():
    """Test DEV login configuration exists."""
    assert DEV_USERNAME is not None
    assert DEV_PASSWORD is not None
    assert len(DEV_USERNAME) > 0
    assert len(DEV_PASSWORD) > 0


def test_authenticate_dev_valid():
    """Test valid DEV authentication."""
    result = authenticate_dev(DEV_USERNAME, DEV_PASSWORD)
    assert result is True


def test_authenticate_dev_empty():
    """Test authentication with empty credentials."""
    result = authenticate_dev("", "")
    assert result is False


def test_authenticate_dev_whitespace():
    """Test authentication with whitespace credentials."""
    result = authenticate_dev("   ", "   ")
    assert result is False


def test_authenticate_dev_none():
    """Test authentication with None credentials."""
    result = authenticate_dev(None, None)
    assert result is False


def test_auth_manager_init():
    """Test AuthManager initialization."""
    auth_manager = AuthManager()
    assert auth_manager is not None
    assert auth_manager.get_current_user() is None


def test_auth_manager_login():
    """Test AuthManager login functionality."""
    auth_manager = AuthManager()
    success = auth_manager.login(DEV_USERNAME, DEV_PASSWORD)
    assert success is True
    assert auth_manager.get_current_user() == DEV_USERNAME


def test_auth_manager_logout():
    """Test AuthManager logout functionality."""
    auth_manager = AuthManager()
    auth_manager.login(DEV_USERNAME, DEV_PASSWORD)
    assert auth_manager.get_current_user() == DEV_USERNAME
    
    auth_manager.logout()
    assert auth_manager.get_current_user() is None


def test_auth_manager_get_current_user():
    """Test AuthManager get_current_user method."""
    auth_manager = AuthManager()
    
    # Initially no user
    assert auth_manager.get_current_user() is None
    
    # After login
    auth_manager.login(DEV_USERNAME, DEV_PASSWORD)
    current_user = auth_manager.get_current_user()
    assert current_user == DEV_USERNAME
    
    # After logout
    auth_manager.logout()
    assert auth_manager.get_current_user() is None
