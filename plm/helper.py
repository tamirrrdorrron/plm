from plm.models import ProductColour, Product, BOM, Material


def get_product_colour_information(pk_product):
    sc = ProductColour.objects.filter(product__pk=pk_product).values(
        'bom',
        'bom__name',
        'colour__name',
        'season__name',
        'product__code',
        'product__pk')
    return sc


def get_product_information(pk_product):
    pi = Product.objects.filter(pk=pk_product).values(
        'code',
        'short_description',
        'designer__name',
        'production_coordinator__name',
        'pattern_maker__name'
    )
    return pi


def get_product_dict(pk_product):
    product_instance = Product.objects.filter(pk=pk_product).first()
    return product_instance


def update_bom(form, product_colour_obj, pk_bom):
    bom_add = form.save(commit=False)
    bom_add.product_colour = product_colour_obj
    bom_add.id = pk_bom
    bom_add.save()
    answers = form.cleaned_data['material']
    for i in answers:
        bom_add.material.add(i)
    bom_add.save()


def remove_material_from_bom(pk_bom, pk_material):
    material_to_remove = Material.objects.filter(pk=pk_material).first()
    bom_to_remove_from = BOM.objects.filter(pk=pk_bom).first()
    bom_to_remove_from.material.remove(material_to_remove)
    return
