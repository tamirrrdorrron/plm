from plm.models import (Colour, Designer, Material, PatternMaker, ProductionCoordinator, Season, Product,
                        MeasurementChart, Size, SizeHeader)

designer = Designer(name='Rosie G').save()

pattern_maker = PatternMaker(name='Janine Johnston').save()

production_coordinator = ProductionCoordinator(name='Vickie Che').save()

Product(code='95600GB', short_description='123', designer=Designer.objects.all().first(),
        pattern_maker=PatternMaker.objects.all().first(),
        production_coordinator=ProductionCoordinator.objects.all().first(), instructions='123').save()

Size(size='6').save()
size_6 = Size.objects.filter(size='6').first()
Size(size='8').save()
size_8 = Size.objects.filter(size='8').first()
Size(size='10').save()
size_10 = Size.objects.filter(size='10').first()
Size(size='12').save()
size_12 = Size.objects.filter(size='12').first()
Size(size='14').save()
size_14 = Size.objects.filter(size='14').first()

SizeHeader(name='6 - 14').save()
size_header = SizeHeader.objects.all().first()
size_header.size.add(size_6)
size_header.size.add(size_8)
size_header.size.add(size_10)
size_header.size.add(size_12)
size_header.size.add(size_14)

MeasurementChart(product=Product.objects.all().first(), size_header=size_header).save()


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
