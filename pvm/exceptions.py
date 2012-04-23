
class BuildingException(Exception):
    """General exception during building"""

class ShellCommandException(Exception):
    """General exception during shell command"""

class UnknownVersionException(Exception):
    """General exception during installing"""
class AlreadyInstalledException(Exception):
    """General exception during installing"""
class NotSupportedVersionException(Exception):
    """General exception during installing"""
    
class CurlFetchException(Exception):
    """Exception curl during fetching"""
