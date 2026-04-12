# PASSWORD ANALYSIS

import zxcvbn
import re

class PasswordAnalyzer:
    def __init__(self):
        self.strength_labels = ["Very Weak", "Weak", "Medium", "Strong", "Very Strong"]

    # ANALYZE PASSWORD STRENGTH USING  ZXCVBN
    def analyse_pass_str(self, password):
        res = zxcvbn.zxcvbn(password)
        return{
            'score' : res['score'],
            'warning': res['feedback']['warning'],
            'suggestions': res['feedback']['suggestions'],
            'crack_time': res['crack_times_display']['offline_slow_hashing_1e4_per_second']
        }
    
    # SECURITY PATTERNS
    def pass_pattern(self, password):
        check = {
            'length': len(password) >= 12,
            'uppercase':bool(re.search(r'[A-Z]', password)), # bool() is used to return "True" or "False"
            'lowercase':bool(re.search(r'[a-z]', password)),
            'numbers': bool(re.search(r'\d', password)),
            "special_char": bool(re.search(r'[!@#$%^&*()<>?{}|,.:"~]', password)),
            'no_common_patterns': not self.common_pattern(password),
            'no_repeating_chars': len(set(password)) / len(password) > 0.6 if password else False # "if password else False" -> Hanldes empty password field.
        }

        return check
    
    # CHECKING FOR PATTERNS THAT ARE NOT SECURE
    def common_pattern(self, password):
        pattern = [
            r'123456', 
            r'1234567890',
            r'password',
            r'qwerty',
            r'abcd123',
            r'(.)\1{2,}', r'123',
            r'2023', r'2024', r'2025', r'2026'
        ]

        return any(re.search(pat, password.lower()) for pat in pattern)
    
    def recommend(self, analysis_res, pattern_check):
        recommendation = []

        if analysis_res['score'] < 3:
            recommendation.append("Consider using a stronger password")
        
        if not pattern_check['length']:
            recommendation.append("use at least 12 characters")
        
        if not pattern_check['uppercase']:
            recommendation.append("Include UpperCase letters")

        if not pattern_check['lowercase']:
            recommendation.append("use lowercase letters")
        
        if not pattern_check['numbers']:
            recommendation.append("Add numbers")
        
        if not pattern_check['special_char']:
            recommendation.append("Add special characters")
        
        if not pattern_check['no_common_patterns']:
            recommendation.append("Do not use common patterns")
        
        if not pattern_check['no_repeating_chars']:
            recommendation.append("Do not use repeating characters")

        recommendation.append(analysis_res['suggestions']) # zxcvbn's suggestions to improve password.

        return recommendation

    # PERFORM FULL IN DEPTH ANALYSIS
    def full_analysis(self, password):

        if not password:
            return{
                'strength_score' : 0,
                'strength_label' : 'Very Weak',
                'Crack_time' : 'instant',
                "warning": "password cannot be empty",
                "pattern_check" : {},
                "recommendations" : ['Please enter a password']
            }
        strength = self.analyse_pass_str(password)
        patterns = self.pass_pattern(password)
        recommendations = self.recommend(strength, patterns)

        return{
            'strength_score': strength['score'],
            'strength_label': self.strength_labels[strength['score']],
            'crack_time' : strength['crack_time'],
            'warning': strength['warning'],
            'pattern_checks': patterns,
            'recommendations': recommendations
        }
    
    # FOR THE GUI
    def res_gui(self, password):
        analysis = self.full_analysis(password)

        warning_text = analysis['warning']
        if not warning_text:
            warning_text = "No Specific warnings...Check Information Below to improve"

        return{
            "strength_test": f"Strength: {analysis['strength_label']} (Score: {analysis['strength_score']}/4)",
            "crack_time": f"Crack Time Estimate: {analysis['crack_time']}",
            "warning": f"Warning: {warning_text}",
            "detailed_results": self.detailed_res(analysis)
        }
    
    def detailed_res(self, analysis):
        results = []
        results.append("\n=---Pattern Checks---=")

        pattern_check = analysis['pattern_checks']
        results.append(f"Length Check (12+ Characters): {pattern_check.get('length')}")
        results.append(f"UpperCase Check: {pattern_check.get('uppercase')}")
        results.append(f"lowercase check: {pattern_check.get('lowercase')}")
        results.append(f"Numbers check: {pattern_check.get('numbers')}")
        results.append(f"Special Characters check: {pattern_check.get('special_char')}")
        results.append(f"No Common Pattern Check: {pattern_check.get('no_common_patterns')}")
        results.append(f"No Repeating Characters Check: {pattern_check.get('no_repeating_chars')}")

        results.append("\n -------RECOMMENDATIONS--------")
        for rec in analysis['recommendations']:
            results.append(f"|{rec}")

        return "\n".join(results)