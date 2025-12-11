#!/usr/bin/env python3
"""
Test script to verify PyProtect's Odoo framework compatibility
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from pyprotect import obfuscate_file, NameCollector, EnhancedObfuscator
import ast

# Sample Odoo model code for testing
SAMPLE_ODOO_MODEL = '''
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    """Sample Odoo model to test obfuscation"""
    _name = 'sale.order'
    _description = 'Sales Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_order desc, name desc'
    
    # Field definitions - should be preserved
    name = fields.Char('Order Reference', required=True, copy=False, readonly=True, default='New')
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    date_order = fields.Datetime('Order Date', required=True, default=fields.Datetime.now)
    amount_total = fields.Monetary('Total', compute='_compute_amount_total', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('sale', 'Sale'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft')
    
    # Compute method - should be preserved
    @api.depends('order_line.price_subtotal')
    def _compute_amount_total(self):
        """Compute the total amount"""
        for order in self:
            total = 0.0
            for line in order.order_line:
                total += line.price_subtotal
            order.amount_total = total
    
    # Onchange method - should be preserved
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        """Update values when partner changes"""
        if self.partner_id:
            self.pricelist_id = self.partner_id.property_product_pricelist
    
    # Constraint - should be preserved
    @api.constrains('date_order')
    def _check_date_order(self):
        """Validate order date"""
        for order in self:
            if order.date_order and order.date_order > fields.Datetime.now():
                raise ValidationError("Order date cannot be in the future")
    
    # Override create - should be preserved
    @api.model_create_multi
    def create(self, vals_list):
        """Override create to set sequence"""
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('sale.order') or 'New'
        return super().create(vals_list)
    
    # Action method - should be preserved
    def action_confirm(self):
        """Confirm the sale order"""
        self.ensure_one()
        if self.state != 'draft':
            raise UserError("Only draft orders can be confirmed")
        self.state = 'sale'
        return True
    
    # Private helper method - can be obfuscated (only used internally)
    def _calculate_tax(self, amount, rate):
        """Internal helper to calculate tax"""
        return amount * rate
    
    # Public method - should be preserved
    def get_order_summary(self):
        """Get order summary for display"""
        self.ensure_one()
        return {
            'name': self.name,
            'partner': self.partner_id.name,
            'total': self.amount_total,
            'state': self.state,
        }
'''

SAMPLE_CONTROLLER = '''
from odoo import http
from odoo.http import request, Response

class SaleController(http.Controller):
    """Sample Odoo controller"""
    
    @http.route('/sale/orders', type='json', auth='user', methods=['GET'])
    def get_orders(self, **kwargs):
        """Get list of sale orders"""
        orders = request.env['sale.order'].search([])
        return orders.read(['name', 'partner_id', 'amount_total'])
    
    @http.route('/sale/order/<int:order_id>', type='json', auth='user')
    def get_order(self, order_id):
        """Get specific order"""
        order = request.env['sale.order'].browse(order_id)
        if not order.exists():
            return {'error': 'Order not found'}
        return order.get_order_summary()
'''

def test_field_detection():
    """Test that Odoo fields are properly detected"""
    print("\n" + "="*60)
    print("TEST 1: Field Name Detection")
    print("="*60)
    
    tree = ast.parse(SAMPLE_ODOO_MODEL)
    collector = NameCollector()
    collector.visit(tree)
    
    # Fields that are DEFINED in this model (should be detected)
    expected_fields = {
        'name', 'partner_id', 'date_order', 'amount_total', 'state'
    }
    
    # Fields that are just REFERENCED but not defined (from related models)
    # These don't need to be detected - only defined fields matter
    referenced_fields = {'order_line', 'pricelist_id'}
    
    detected = collector.field_names
    
    print(f"Expected defined fields: {sorted(expected_fields)}")
    print(f"Detected fields: {sorted(detected)}")
    
    # Check if all defined fields are detected
    missing = expected_fields - detected
    extra = detected - expected_fields - referenced_fields
    
    if missing:
        print(f"❌ Missing defined fields: {missing}")
    
    # Extra detected fields are OK - could be from method names or related fields
    if extra:
        print(f"ℹ️  Additional fields detected: {extra}")
    
    if not missing:
        print("✅ PASSED: All defined fields detected")
        return True
    else:
        print(f"❌ FAILED: {len(missing)} field(s) not detected")
        return False

def test_method_detection():
    """Test that Odoo methods are properly detected"""
    print("\n" + "="*60)
    print("TEST 2: Method Name Detection")
    print("="*60)
    
    tree = ast.parse(SAMPLE_ODOO_MODEL)
    collector = NameCollector()
    collector.visit(tree)
    
    # Methods that should be preserved
    preserved_methods = {
        '_compute_amount_total', '_onchange_partner_id', 
        '_check_date_order', 'create', 'action_confirm',
        'get_order_summary'
    }
    
    # Methods that can be obfuscated
    obfuscatable_methods = {
        '_calculate_tax'  # Private helper, only used internally
    }
    
    print(f"Methods that should be preserved: {sorted(preserved_methods)}")
    print(f"Methods that can be obfuscated: {sorted(obfuscatable_methods)}")
    
    detected_methods = collector.method_names
    
    all_passed = True
    for method in preserved_methods:
        should_preserve = detected_methods.get(method, False)
        status = "✅" if should_preserve else "❌"
        print(f"{status} {method}: {'PRESERVED' if should_preserve else 'OBFUSCATED'}")
        if not should_preserve:
            all_passed = False
    
    # Note: _calculate_tax could be preserved or obfuscated based on settings
    # If it's preserved, that's fine (safer approach)
    
    if all_passed:
        print("✅ PASSED: All critical methods marked for preservation")
        return True
    else:
        print("❌ FAILED: Some critical methods not preserved")
        return False

def test_obfuscation_preserves_structure():
    """Test that obfuscation maintains code structure"""
    print("\n" + "="*60)
    print("TEST 3: Code Structure Preservation")
    print("="*60)
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = Path(tmpdir) / "test_model.py"
        output_file = Path(tmpdir) / "test_model_obf.py"
        
        # Write sample code
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(SAMPLE_ODOO_MODEL)
        
        # Obfuscate
        print("Obfuscating code...")
        try:
            success = obfuscate_file(
                str(input_file),
                str(output_file),
                bind_machine=False,
                preserve_api=True
            )
            
            if not success:
                print("❌ FAILED: Obfuscation failed")
                return False
            
            # Read obfuscated code
            with open(output_file, 'r', encoding='utf-8') as f:
                obfuscated = f.read()
            
            # Check that critical elements are preserved
            checks = [
                ("Class name preserved", "class SaleOrder" in obfuscated),
                ("Model _name preserved", "_name = 'sale.order'" in obfuscated or "_name = " in obfuscated),
                ("Field names preserved", "partner_id" in obfuscated),
                ("Compute method preserved", "_compute_amount_total" in obfuscated),
                ("Onchange method preserved", "_onchange_partner_id" in obfuscated),
                ("Action method preserved", "action_confirm" in obfuscated),
                ("Odoo imports preserved", "from odoo import" in obfuscated),
                ("Decorator preserved", "@api.depends" in obfuscated or "api.depends" in obfuscated),
            ]
            
            all_passed = True
            for check_name, passed in checks:
                status = "✅" if passed else "❌"
                print(f"{status} {check_name}")
                if not passed:
                    all_passed = False
            
            # Try to parse the obfuscated code to ensure it's valid Python
            try:
                ast.parse(obfuscated)
                print("✅ Obfuscated code is valid Python")
            except SyntaxError as e:
                print(f"❌ Obfuscated code has syntax error: {e}")
                all_passed = False
            
            if all_passed:
                print("✅ PASSED: Code structure properly preserved")
                return True
            else:
                print("❌ FAILED: Some critical elements not preserved")
                return False
                
        except Exception as e:
            print(f"❌ FAILED: Exception during obfuscation: {e}")
            import traceback
            traceback.print_exc()
            return False

def test_controller_obfuscation():
    """Test that HTTP controllers are properly handled"""
    print("\n" + "="*60)
    print("TEST 4: Controller Obfuscation")
    print("="*60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = Path(tmpdir) / "test_controller.py"
        output_file = Path(tmpdir) / "test_controller_obf.py"
        
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(SAMPLE_CONTROLLER)
        
        try:
            success = obfuscate_file(
                str(input_file),
                str(output_file),
                bind_machine=False,
                preserve_api=True
            )
            
            if not success:
                print("❌ FAILED: Obfuscation failed")
                return False
            
            with open(output_file, 'r', encoding='utf-8') as f:
                obfuscated = f.read()
            
            checks = [
                ("Controller class preserved", "class SaleController" in obfuscated),
                ("HTTP route preserved", "@http.route" in obfuscated or "http.route" in obfuscated),
                ("Controller methods preserved", "get_orders" in obfuscated and "get_order" in obfuscated),
                ("Request object preserved", "request" in obfuscated),
            ]
            
            all_passed = True
            for check_name, passed in checks:
                status = "✅" if passed else "❌"
                print(f"{status} {check_name}")
                if not passed:
                    all_passed = False
            
            if all_passed:
                print("✅ PASSED: Controller properly handled")
                return True
            else:
                print("❌ FAILED: Controller not properly preserved")
                return False
                
        except Exception as e:
            print(f"❌ FAILED: Exception during obfuscation: {e}")
            import traceback
            traceback.print_exc()
            return False

def test_manifest_handling():
    """Test that manifest files are skipped"""
    print("\n" + "="*60)
    print("TEST 5: Manifest File Handling")
    print("="*60)
    
    manifest_content = '''{
    'name': 'Test Module',
    'version': '1.0',
    'depends': ['base', 'sale'],
    'data': [
        'views/templates.xml',
    ],
}'''
    
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = Path(tmpdir) / "__manifest__.py"
        output_file = Path(tmpdir) / "dist" / "__manifest__.py"
        output_file.parent.mkdir(exist_ok=True)
        
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(manifest_content)
        
        try:
            success = obfuscate_file(
                str(input_file),
                str(output_file),
                bind_machine=False,
                preserve_api=True
            )
            
            if not success:
                print("❌ FAILED: Obfuscation failed")
                return False
            
            with open(output_file, 'r', encoding='utf-8') as f:
                obfuscated = f.read()
            
            # Manifest should be unchanged (no encryption runtime)
            is_unchanged = '_decrypt_str' not in obfuscated
            
            if is_unchanged:
                print("✅ PASSED: Manifest file was skipped (copied as-is)")
                return True
            else:
                print("❌ FAILED: Manifest file was obfuscated")
                return False
                
        except Exception as e:
            print(f"❌ FAILED: Exception: {e}")
            return False

def run_all_tests():
    """Run all compatibility tests"""
    print("\n" + "="*60)
    print("PyProtect - Odoo Compatibility Test Suite")
    print("="*60)
    
    tests = [
        ("Field Detection", test_field_detection),
        ("Method Detection", test_method_detection),
        ("Code Structure", test_obfuscation_preserves_structure),
        ("Controller Handling", test_controller_obfuscation),
        ("Manifest Handling", test_manifest_handling),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"\n❌ TEST '{test_name}' CRASHED: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print("\n" + "-"*60)
    print(f"Total: {passed_count}/{total_count} tests passed")
    print("="*60)
    
    if passed_count == total_count:
        print("\n🎉 ALL TESTS PASSED! PyProtect is Odoo-compatible!")
        return 0
    else:
        print(f"\n⚠️  {total_count - passed_count} test(s) failed. Review the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())

