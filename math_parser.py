import sympy as sp
from sympy import symbols, sympify, SympifyError
import numpy as np
import re

class MathParser:
    """
    Advanced mathematical expression parser supporting various equation formats
    """
    
    def __init__(self):
        self.x, self.y, self.z, self.t = symbols('x y z t')
        self.common_functions = {
            'sin': sp.sin,
            'cos': sp.cos,
            'tan': sp.tan,
            'exp': sp.exp,
            'log': sp.log,
            'ln': sp.log,
            'sqrt': sp.sqrt,
            'abs': sp.Abs,
            'pi': sp.pi,
            'e': sp.E
        }
    
    def parse_equation(self, equation_str):
        """
        Parse a mathematical equation string into a SymPy expression
        
        Args:
            equation_str (str): Mathematical equation as string
            
        Returns:
            sympy.Expr: Parsed expression or None if invalid
        """
        try:
            # Clean and prepare the equation string
            cleaned_eq = self._clean_equation(equation_str)
            
            # Handle different equation formats
            if '=' in cleaned_eq:
                # Handle equations with explicit z = f(x,y) or y = f(x) format
                left, right = cleaned_eq.split('=', 1)
                if left.strip() in ['z', 'y', 'f']:
                    expression = right.strip()
                else:
                    # Assume it's an implicit equation, move everything to one side
                    expression = f"({left}) - ({right})"
            else:
                expression = cleaned_eq
            
            # Replace common mathematical notation
            expression = self._replace_math_notation(expression)
            
            # Parse with SymPy
            parsed_expr = sympify(expression, locals=self.common_functions)
            
            return parsed_expr
            
        except (SympifyError, ValueError, TypeError) as e:
            print(f"Parsing error: {e}")
            return None
    
    def _clean_equation(self, equation_str):
        """Clean and standardize equation string"""
        # Remove whitespace
        cleaned = equation_str.strip()
        
        # Replace common math symbols
        replacements = {
            '^': '**',  # Power notation
            '×': '*',   # Multiplication
            '÷': '/',   # Division
            '−': '-',   # Minus sign
        }
        
        for old, new in replacements.items():
            cleaned = cleaned.replace(old, new)
        
        return cleaned
    
    def _replace_math_notation(self, expression):
        """Replace mathematical notation with SymPy-compatible syntax"""
        # Handle implicit multiplication (e.g., 2x -> 2*x)
        expression = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expression)
        expression = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', expression)
        expression = re.sub(r'(\))([a-zA-Z\(])', r'\1*\2', expression)
        expression = re.sub(r'([a-zA-Z\)])(\()', r'\1*\2', expression)
        
        # Handle function notation
        function_replacements = {
            'arcsin': 'asin',
            'arccos': 'acos',
            'arctan': 'atan',
            'sinh': 'sinh',
            'cosh': 'cosh',
            'tanh': 'tanh',
        }
        
        for old, new in function_replacements.items():
            expression = expression.replace(old, new)
        
        return expression
    
    def validate_expression(self, expression):
        """
        Validate if an expression is mathematically sound
        
        Args:
            expression (sympy.Expr): Expression to validate
            
        Returns:
            dict: Validation results with status and messages
        """
        validation_result = {
            'valid': True,
            'warnings': [],
            'errors': []
        }
        
        try:
            # Check for undefined symbols
            free_symbols = expression.free_symbols
            expected_symbols = {self.x, self.y, self.z, self.t}
            unexpected_symbols = free_symbols - expected_symbols
            
            if unexpected_symbols:
                validation_result['warnings'].append(
                    f"Unexpected symbols found: {unexpected_symbols}"
                )
            
            # Check for potential division by zero
            if expression.has(1/self.x) or expression.has(1/self.y):
                validation_result['warnings'].append(
                    "Expression contains division by variables - check for singularities"
                )
            
            # Test evaluation at a few points
            test_points = [(0, 0), (1, 1), (-1, -1), (0.5, 0.5)]
            for point in test_points:
                try:
                    if len(free_symbols) >= 2:
                        result = expression.subs([(self.x, point[0]), (self.y, point[1])])
                    elif len(free_symbols) == 1:
                        result = expression.subs(list(free_symbols)[0], point[0])
                    
                    # Check if result is numeric
                    complex_result = complex(result.evalf())
                    if not np.isfinite(complex_result.real) or not np.isfinite(complex_result.imag):
                        validation_result['warnings'].append(
                            f"Expression may be undefined at point {point}"
                        )
                except Exception as e:
                    validation_result['warnings'].append(
                        f"Evaluation error at point {point}: {str(e)}"
                    )
            
        except Exception as e:
            validation_result['valid'] = False
            validation_result['errors'].append(f"Validation error: {str(e)}")
        
        return validation_result
    
    def extract_domain_info(self, expression):
        """
        Extract domain information from expression
        
        Args:
            expression (sympy.Expr): Expression to analyze
            
        Returns:
            dict: Domain information
        """
        domain_info = {
            'variables': list(expression.free_symbols),
            'restrictions': [],
            'suggested_range': {'x': (-10, 10), 'y': (-10, 10)}
        }
        
        # Check for logarithmic functions
        if expression.has(sp.log):
            domain_info['restrictions'].append("Logarithmic functions require positive arguments")
        
        # Check for square roots
        if expression.has(sp.sqrt):
            domain_info['restrictions'].append("Square root functions require non-negative arguments")
        
        # Check for rational functions
        denominators = []
        for term in sp.preorder_traversal(expression):
            if term.is_Pow and term.exp.is_negative:
                denominators.append(term.base)
        
        if denominators:
            domain_info['restrictions'].append(
                f"Avoid zeros in denominators: {denominators}"
            )
        
        return domain_info
    
    def convert_to_lambda(self, expression, variables=None):
        """
        Convert SymPy expression to lambda function for numerical evaluation
        
        Args:
            expression (sympy.Expr): Expression to convert
            variables (list): List of variables in order
            
        Returns:
            function: Lambda function for numerical evaluation
        """
        if variables is None:
            free_symbols = list(expression.free_symbols)
            # Sort symbols by name for consistency
            variables = sorted(free_symbols, key=str)
        
        try:
            return sp.lambdify(variables, expression, 'numpy')
        except Exception as e:
            print(f"Lambda conversion error: {e}")
            return None
