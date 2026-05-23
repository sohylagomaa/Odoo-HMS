{
    'name': 'HMS - Hospital Management System',
    'version': '1.0',
    'category': 'Healthcare',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/hms_department_views.xml',
        'views/hms_doctors_views.xml',
        'views/hms_patient_views.xml',
    ],
    'installable': True,
    'application': True,
    'sequence': 1,
}