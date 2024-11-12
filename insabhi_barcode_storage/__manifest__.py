{
    'name': 'Insabhi Barcode Storage',
    'author': 'Insabhi',
    'depends': ['base', 'web', 'stock', 'stock_barcode'],
    'data': [
            'views/main_menu.xml',
            'views/location_add_section.xml',
            'views/warehouse_page.xml',
    ],
    'assets': {
            'web.assets_backend': [
                'insabhi_barcode_storage/static/src/js/barcodeMenu.js',
                'insabhi_barcode_storage/static/src/xml/barcode_menu.xml',
        ]
    },

}