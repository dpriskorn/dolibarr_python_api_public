# """
# {
#     'baseOptions_0_selected_code': 'PT101081',
#     'baseOptions_0_selected_name': 'Gängtapp TAP-10 10mm till ex. bakväxelöra',
#     'baseOptions_0_selected_priceData_currencyIso': 'SEK',
#     'baseOptions_0_selected_priceData_formattedValue': '89,00 kr',
#     'baseOptions_0_selected_priceData_priceType': 'BUY',
#     'baseOptions_0_selected_priceData_value': 89.0,
#     'baseOptions_0_selected_stock_stockLevel': 40,
#     'baseOptions_0_selected_stock_stockLevelStatus': 'backorder',
#     'baseOptions_0_selected_url':
# '/Shimano-Europe-Bike-B2B/Tillbeh%C3%B6r-cykel/VERKTYG/VERKTYG/G%C3%A4ngtapp-TAP
# -10-10mm/p/PT101081',
#     'baseOptions_0_selected_variantOptionQualifiers': [],
#     'baseOptions_0_variantType': 'GenericVariantProduct',
#     'baseProdCategory': 'cg4B2BEU_Tools',
#     'baseProduct': 'P-PTWFT',
#     'baseProductName': 'Gängtapp TAP-10 10mm',
#     'brand_code': 'PK',
#     'brand_name': 'Park Tool',
#     'classifications_0_code': 'clcg3SOBSEHCTools',
#     'classifications_0_features_0_code':
# 'shimanoBikeClassification/1.0/clcg3SOBSEHCTools.clsehaproductapplication',
#     'classifications_0_features_0_comparable': True,
#     'classifications_0_features_0_featureValues_0_value': 'TAP-10',
#     'classifications_0_features_0_name': 'Produktapplicering',
#     'classifications_0_features_0_range': False,
#     'classifications_0_features_1_code':
# 'shimanoBikeClassification/1.0/clcg3SOBSEHCTools.clsehanroftools',
#     'classifications_0_features_1_comparable': True,
#     'classifications_0_features_1_featureValues_0_value': 'Not Applicable',
#     'classifications_0_features_1_name': 'Antal Verktyg',
#     'classifications_0_features_1_range': False,
#     'classifications_0_name': 'SEH AgencyBrand Cycling Tools',
#     'code': 'PT101081',
#     'configurable': False,
#     'explodedViewIdList': [],
#     'groupset': False,
#     'hasVariants': False,
#     'images_0_altText': 'Gängtapp TAP-10 10mm till ex. bakväxelöra',
#     'images_0_format': 'product',
#     'images_0_imageType': 'PRIMARY',
#     'images_0_url':
# 'https://dassets.shimano.com/content/dam/global/cg1SEHAC/parktool/products/TAP-1
# 0_001.jpg',
#     'inStockFlag': False,
#     'leadTime': 2,
#     'manuals_categorizedManualsList': [],
#     'name': 'Gängtapp TAP-10 10mm till ex. bakväxelöra',
#     'purchasable': True,
#     'showOrderFormButton': True,
#     'superCategories_0_code': 'cgvvc_SEHAC_clSEHAProductApplication_tap-10',
#     'superCategories_0_name': 'TAP-10',
#     'superCategories_0_parentCategoryName': 'Produktapplicering',
#     'superCategories_0_type': 'VariantValueCategory',
#     'superCategories_0_url':
# '//E-T-R-T-O-Storlek/Franska-storlekar/D%C3%A4ckstorlek-tum/Tillbeh%C3%B6r/L%C3%
# A5styp/S%C3%A4kerhetsniv%C3%A5/Cykeltillbeh%C3%B6r-f%C3%A4rg/F%C3%A4rg/Korgstorl
# ek/Cykeltillbeh%C3%B6r-storlek/Cykelkomponenter-material/Sadelvikt/Cykelkomponen
# ter-material/Tr%C3%A4nartyp/flaska-inneh%C3%A5ll/Cykelkomponenter-material/D%C3%
# A4ckstorlek-tum/Uppkopplingsbar/Computer-type/Position/Hjulstorlek/Broms-typ/N%C
# 3%A4ring-smak/Skydd-storlek/Cykeltillbeh%C3%B6r-storlek/Sk%C3%B6tselr%C3%A5d/F%C
# 3%B6rpackning/Listade-Funktioner/D%C3%A4ckbredd/Valve-Brand/Valve-Length/V%C3%A4
# ska-inneh%C3%A5ll/F%C3%A4stanordning-till-nom-storlek/F%C3%A4stanordning-Diamete
# r/Verkstad-bredd/Verkstad-Position/Content/Ventiltyp/Lumen-Indicator/M%C3%A5tt/P
# roduktapplicering/TAP-10/c/cgvvc_SEHAC_clSEHAProductApplication_tap-10',
#     'upc': '763477007650',
#     'url':
# '/Shimano-Europe-Bike-B2B/Tillbeh%C3%B6r-cykel/VERKTYG/VERKTYG/G%C3%A4ngtapp-TAP
# -10-10mm/p/PT101081'
# }
# """
# from typing import Optional
#
# from pydantic import BaseModel
#
#
# class ShimanoProductOptions(MyBaseModel):
#     """This models a flattened json response from ShimanoProductOptions"""
#
#     baseOptions_0_selected_name: str  # more detailed swedish name
#     baseOptions_0_selected_priceData_value: float
#     baseOptions_0_selected_stock_stockLevel: int
#     baseProductName: str  # swedish name
#     brand_name: str
#     images_0_url: Optional[str]  # this is a complete url
#     leadTime: int  # days
#     upc: int = 0
