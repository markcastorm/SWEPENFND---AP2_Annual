#!/usr/bin/env python3
"""
Test the Perfect LLM Parser for 100% accuracy validation
"""

import os
import sys
import logging

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test direct execution
if __name__ == "__main__":
    try:
        from perfect_llm_parser import PerfectLLMParser
        import config
        
        print("=" * 80)
        print("TESTING PERFECT LLM PARSER FOR 100% ACCURACY")
        print("=" * 80)
        
        # Test with the project PDF
        if os.path.exists('AnnualReport2024.pdf'):
            print("✓ Found AnnualReport2024.pdf")
            
            # Initialize perfect parser
            print("\n🚀 Initializing Perfect LLM Parser...")
            parser = PerfectLLMParser()
            
            # Test each section individually
            sections = ['fund_capital', 'asset_allocation', 'real_assets', 'bonds']
            results = {}
            
            print("\n📊 Testing Each Section:")
            print("-" * 50)
            
            for section in sections:
                print(f"\n🎯 Testing {section}...")
                try:
                    data = parser.extract_section_with_precision('AnnualReport2024.pdf', section)
                    results[section] = data
                    
                    expected = len(parser.get_field_mapping(section))
                    actual = len(data)
                    accuracy = (actual / expected * 100) if expected > 0 else 0
                    
                    print(f"   📈 Result: {actual}/{expected} fields ({accuracy:.1f}%)")
                    
                    # Show sample values
                    if data:
                        sample_keys = list(data.keys())[:3]
                        for key in sample_keys:
                            print(f"   📌 {key.split('.')[-2]}: {data[key]}")
                    
                except Exception as e:
                    print(f"   ❌ Error: {e}")
                    results[section] = {}
            
            print("\n" + "=" * 80)
            print("📋 FINAL ACCURACY REPORT")
            print("=" * 80)
            
            total_expected = 0
            total_actual = 0
            
            for section in sections:
                expected = len(parser.get_field_mapping(section))
                actual = len(results.get(section, {}))
                accuracy = (actual / expected * 100) if expected > 0 else 0
                
                total_expected += expected
                total_actual += actual
                
                status = "✅ PERFECT" if accuracy == 100 else "⚠️  PARTIAL" if accuracy > 0 else "❌ FAILED"
                print(f"{status} {section:20} {actual:2d}/{expected:2d} fields ({accuracy:5.1f}%)")
            
            final_accuracy = (total_actual / total_expected * 100) if total_expected > 0 else 0
            
            print("-" * 80)
            print(f"🎯 OVERALL ACCURACY: {total_actual}/{total_expected} fields ({final_accuracy:.1f}%)")
            
            if final_accuracy == 100:
                print("🏆 PERFECT EXTRACTION ACHIEVED!")
            elif final_accuracy >= 90:
                print("🥈 EXCELLENT EXTRACTION!")
            elif final_accuracy >= 70:
                print("🥉 GOOD EXTRACTION - NEEDS REFINEMENT")
            else:
                print("🔧 REQUIRES IMPROVEMENT")
            
            print("\n📊 Expected Values for Validation:")
            print("-" * 50)
            print("Fund Capital: 458884, -2024, 34868")
            print("Asset Allocation Strategic: 9, 20, 10, 10, 18, 13, 11, 5, 4, 100, 31")
            print("Asset Allocation Actual: 10, 20, 10, 13, 18, 11, 10, 5, 4, -1, 100, 24")
            print("Real Assets: 13, 59, 28, 42, 5, 5, 10, 30, 4, 4")
            print("Bonds 2024: 2434, 92, 546, 3090, 277, 49001, 73895, 129335, 115009, 2678, 11648")
            
        else:
            print("❌ AnnualReport2024.pdf not found")
            
    except Exception as e:
        print(f"💥 Error testing parser: {e}")
        import traceback
        traceback.print_exc()