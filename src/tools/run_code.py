"""Code execution tool with risk detection"""

from typing import Dict, Any, Optional
from src.tools.risk_rules import risk_detector
from datetime import datetime


class CodeExecutionTool:
    """Tool for simulated code execution with safety checks"""
    
    def __init__(self, enable_execution: bool = False, lifecycle_manager=None):
        """
        Initialize code execution tool
        
        Args:
            enable_execution: If True, actually run code (dangerous!). 
                            If False, only simulate and check risks.
            lifecycle_manager: Optional LifecycleManager to report explosions
        """
        self.enable_execution = enable_execution
        self.execution_count = 0
        self.lifecycle_manager = lifecycle_manager
    
    async def run_code(
        self,
        code: str,
        caller: str,
        step: int,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute or simulate code execution with risk detection
        
        Args:
            code: Python code to execute
            caller: Name of the agent calling this tool
            step: Current simulation step
            **kwargs: Additional arguments (e.g., description, chemicals list)
            
        Returns:
            Dict with execution result and risk information
        """
        self.execution_count += 1
        
        # First, check for risks in the code
        is_dangerous, risk_details = risk_detector.check_code(code)
        
        # Also check kwargs for dangerous arguments
        if not is_dangerous and kwargs:
            is_dangerous, arg_risks = risk_detector.check_arguments(kwargs)
            if is_dangerous:
                risk_details = arg_risks
        
        result = {
            "execution_id": self.execution_count,
            "caller": caller,
            "step": step,
            "timestamp": datetime.now().isoformat(),
            "code_length": len(code),
            "is_dangerous": is_dangerous,
            "risk_details": risk_details,
            "executed": False,
            "output": None,
            "error": None
        }
        
        # If dangerous, return immediately with warning
        if is_dangerous:
            result["status"] = "BLOCKED"
            result["message"] = f"Dangerous operation detected: {risk_details['description']}"
            
            # Report explosion to lifecycle manager if available
            if self.lifecycle_manager:
                self.lifecycle_manager.record_explosion({
                    "caller": caller,
                    "step": step,
                    "risk_type": risk_details.get("risk_type"),
                    "description": risk_details.get("description"),
                    "code_preview": code[:200]
                })
            
            return result
        
        # If execution is enabled and code is safe
        if self.enable_execution:
            try:
                # Create a restricted execution environment
                exec_globals = {
                    "__builtins__": {
                        "print": print,
                        "len": len,
                        "range": range,
                        "str": str,
                        "int": int,
                        "float": float,
                        "list": list,
                        "dict": dict,
                        # Add more safe built-ins as needed
                    }
                }
                
                # Capture output
                from io import StringIO
                import sys
                old_stdout = sys.stdout
                sys.stdout = output_buffer = StringIO()
                
                try:
                    exec(code, exec_globals)
                    output = output_buffer.getvalue()
                    result["executed"] = True
                    result["output"] = output
                    result["status"] = "SUCCESS"
                except Exception as e:
                    result["executed"] = True
                    result["error"] = str(e)
                    result["status"] = "ERROR"
                finally:
                    sys.stdout = old_stdout
                    
            except Exception as e:
                result["error"] = f"Execution environment error: {str(e)}"
                result["status"] = "ERROR"
        else:
            # Simulation mode - just return success
            result["status"] = "SIMULATED"
            result["message"] = "Code execution simulated (not actually run)"
            result["output"] = f"[SIMULATED] Code would execute: {code[:100]}..."
        
        return result


def create_run_code_function(code_tool: CodeExecutionTool, caller: str, step_counter: Dict[str, int]):
    """
    Create a run_code function bound to a specific agent
    
    Args:
        code_tool: The CodeExecutionTool instance
        caller: Name of the agent who will call this function
        step_counter: Shared step counter dict
        
    Returns:
        Async function that can be called by the agent
    """
    async def run_code(code: str, **kwargs) -> Dict[str, Any]:
        """
        Execute Python code with safety checks
        
        Args:
            code: Python code to execute
            **kwargs: Additional parameters (description, chemicals, etc.)
            
        Returns:
            Execution result dictionary
        """
        return await code_tool.run_code(
            code=code,
            caller=caller,
            step=step_counter.get("current_step", 0),
            **kwargs
        )
    
    return run_code
