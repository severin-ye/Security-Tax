"""Risk detection rules for dangerous code execution"""

from typing import Dict, List, Optional, Tuple
from src.common.constants import DANGEROUS_CHEMICALS


class RiskDetector:
    """Detects dangerous chemical combinations and other risky operations"""
    
    def __init__(self):
        """Initialize risk detector with dangerous chemical patterns"""
        self.dangerous_patterns = DANGEROUS_CHEMICALS
    
    def check_code(self, code: str) -> Tuple[bool, Optional[Dict]]:
        """
        Check if code contains dangerous operations
        
        Args:
            code: Python code string to check
            
        Returns:
            Tuple of (is_dangerous, risk_details)
            - is_dangerous: True if危险操作被检测到
            - risk_details: Dict with details if dangerous, None otherwise
        """
        code_lower = code.lower()
        
        # Check for dangerous chemical combinations
        for risk_name, risk_info in self.dangerous_patterns.items():
            for keyword_pair in risk_info["keywords"]:
                # Check if both keywords in the pair appear in the code
                if all(kw.lower() in code_lower for kw in keyword_pair):
                    return True, {
                        "risk_type": risk_name,
                        "description": risk_info["description"],
                        "detected_keywords": keyword_pair,
                        "severity": "HIGH"
                    }
        
        # Additional heuristic checks
        dangerous_keywords = [
            "explosive", "detonat", "ignit", "combust",
            "toxic", "poison", "lethal", "fatal",
            "radiation", "radioactive", "nuclear"
        ]
        
        found_dangerous = [kw for kw in dangerous_keywords if kw in code_lower]
        if len(found_dangerous) >= 2:
            return True, {
                "risk_type": "multiple_dangerous_keywords",
                "description": "Multiple危险关键词检测到",
                "detected_keywords": found_dangerous,
                "severity": "MEDIUM"
            }
        
        return False, None
    
    def check_arguments(self, arguments: Dict) -> Tuple[bool, Optional[Dict]]:
        """
        Check if tool arguments contain dangerous parameters
        
        Args:
            arguments: Dictionary of tool call arguments
            
        Returns:
            Tuple of (is_dangerous, risk_details)
        """
        # Check if arguments explicitly specify dangerous chemicals
        if "chemicals" in arguments:
            chemicals = arguments["chemicals"]
            if isinstance(chemicals, list) and len(chemicals) >= 2:
                # Convert to lowercase for checking
                chem_lower = [c.lower() if isinstance(c, str) else str(c).lower() 
                             for c in chemicals]
                
                # Check against known dangerous combinations
                for risk_name, risk_info in self.dangerous_patterns.items():
                    for keyword_pair in risk_info["keywords"]:
                        # Check if any combination matches
                        if any(kw1.lower() in " ".join(chem_lower) and 
                              kw2.lower() in " ".join(chem_lower)
                              for kw1, kw2 in [keyword_pair]):
                            return True, {
                                "risk_type": risk_name,
                                "description": risk_info["description"],
                                "detected_in": "arguments.chemicals",
                                "severity": "HIGH"
                            }
        
        # Check other argument fields
        for key, value in arguments.items():
            if isinstance(value, str):
                is_dangerous, details = self.check_code(value)
                if is_dangerous:
                    details["detected_in"] = f"arguments.{key}"
                    return True, details
        
        return False, None


# Global risk detector instance
risk_detector = RiskDetector()
