from plm.models import StyleColourway, Product


def get_style_colourway_information(style_code):
    sc = StyleColourway.objects.filter(product__code=style_code).values(
        'bom',
        'bom__name',
        'colourway__name',
        'season__name',
        'product__code')
    return sc


def get_product_information(style_code):
    pi = Product.objects.filter(code=style_code).values(
        'code',
        'short_description',
        'designer__name',
        'production_coordinator__name',
        'pattern_maker__name'
    )
    return pi


def get_product_image(style_code):
    image = Product.objects.filter(code=style_code)[0]
    return image


def get_style_code_dict(style_code):
    style_dict = {'style_code': style_code}
    return style_dict


def update_bom(form, style_colourway_obj, bom_id):
    bom_add = form.save(commit=False)
    bom_add.style_colourway = style_colourway_obj
    bom_add.id = bom_id
    bom_add.save()
    answers = form.cleaned_data['material']
    for i in answers:
        bom_add.material.add(i)
    bom_add.save()
