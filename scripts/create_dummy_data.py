from plm.models import Colourway, Material, Season, Designer, PatternMaker, ProductionCoordinator

Designer(name='Rosie G').save()
PatternMaker(name='Janine Johnston').save()
ProductionCoordinator(name='Vickie Che').save()
Colourway(code='RED', name='Red').save()
Colourway(code='BLK', name='Black').save()
Season(code='JAN19', name='January 2019').save()
Season(code='FEB19', name='February 2019').save()
Season(code='MAR19', name='March 2019').save()
Material(code='MAT001', name='Lace', photo='materials/main.jpg').save()
Material(code='MAT002', name='Woven', photo='materials/main.jpg').save()
Material(code='MAT003', name='Knit', photo='materials/main.jpg').save()
