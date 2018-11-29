from plm.models import (Colour, Designer, Material, PatternMaker,
                        ProductionCoordinator, Season)

Designer(name='Rosie G').save()
PatternMaker(name='Janine Johnston').save()
ProductionCoordinator(name='Vickie Che').save()
Colour(code='RED', name='Red', notes='like the formula 1').save()
Colour(code='BLK', name='Black', notes='use this only for colourways').save()
Season(code='JAN19', name='January 2019').save()
Season(code='FEB19', name='February 2019').save()
Season(code='MAR19', name='March 2019').save()
Material(code='MAT001',
         name='Lace',
         content='100% polyester',
         weight='200grams',
         vendor_mill='YUN',
         vendor_ref='Pad 1, ref 62',
         photo='materials/main.jpg').save()
Material(code='MAT002',
         name='Woven',
         content='70% cotton, 30% polyester',
         weight='100grams',
         vendor_mill='XIU',
         vendor_ref='#4567',
         photo='materials/main.jpg').save()
Material(code='MAT003',
         name='Knit',
         content='100% cotton',
         weight='350grams',
         vendor_mill='YUN',
         vendor_ref='#AB3321-BAR',
         photo='materials/main.jpg').save()