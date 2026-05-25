{
    'name': 'HMS - Hospital Management System',
    'version': '1.0',
    'author': 'sohyla',
    'license': 'LGPL-3',
    'category': 'Healthcare',
    'depends': ['base', 'contacts', 'sale_management'],
    'data': [
        'security/hms_groups.xml',
        'security/ir.model.access.csv',
        'views/hms_department_views.xml',
        'views/hms_doctors_views.xml',
        'views/hms_patient_views.xml',
        'views/inherited_res_partner_views.xml',
        'reports/hms_patient_report.xml',
    ],
    'installable': True,
    'application': True,
}