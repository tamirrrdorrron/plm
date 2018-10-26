from plm.models import BOM


#this view assumes that the BOM object already exists and you are just adding materials to it
# def add_material_to_bom(bom_id, qs_material):
#     bom = BOM.objects.filter(id=bom_id)
#     bom[0].material.set(qs_material)
#     return bom[0].material.all()


def add_bom(form, seasonal_colourway_id):
    bom_add = form.save(commit=False)
    bom_add.seasonal_colourway = seasonal_colourway_id
    bom_add.save()
    answers = form.cleaned_data['material']
    for i in answers:
        bom_add.material.add(i)
    bom_add.save()
