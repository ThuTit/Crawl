
# insert_promotion_warning = "INSERT INTO `price_promotion_management`.`promotion_warnings` (`created_at`, `updated_at`, `object`, `object_id`, `is_expired`, `data`) VALUES ('2019-07-17 02:22:08.904665', '2019-07-17 02:22:08.904665', 'promotion', 53, 0, '{\"skus_out_of_stock\": [\"1200108\"]}')"
import datetime

data = """{
    "type": {
        "code": "ltqxbanpdj",
        "name": "nahvcenvqa"
    },
    "sku": "1254872016",
    "objective": {
        "code": "jnijxbakoi",
        "name": "mmlzrlkukx"
    },
    "warranty": {
        "description": "czhcyqqmtu",
        "months": 389
    },
    "seller_categories": [
        {
            "level": 7747229,
            "parent_id": 8891126,
            "code": "ntvaqitjup",
            "name": "Charles Henderson",
            "id": 4486359
        }
    ],
    "seller_id": 1036460,
    "name": "Donald Schultz",
    "id": 9298359,
    "created_at": "2018-07-30T20:24:30Z",
    "attribute_set": {
        "id": 9259544,
        "name": "Chase Lawson"
    },
    "color": {
        "code": "ywulznemms",
        "name": "weecuhuiyl"
    },
    "attribute_groups": [
        {
            "parent_id": 1250431,
            "value": "edqmpiniuc",
            "name": "Ricky Lee",
            "id": 622,
            "priority": 5
        }
    ],
    "tags": null,
    "channels": [
        {
            "id": 4016801,
            "code": "yydovennww",
            "name": "wqamvsilyz"
        }
    ],
    "images": [
        {
            "label": "fszzollnyq",
            "url": "dgppyqwiya",
            "priority": 1
        },
        {
            "label": "akumtnudhs",
            "url": "aapxeyvzts",
            "priority": 6
        }
    ],
    "categories": [
        {
            "level": 6397270,
            "parent_id": 2908904,
            "code": "nukmwazbgp",
            "name": "Terry Torres",
            "id": 9046892
        }
    ],
    "brand": {
        "id": 4382093,
        "code": "gijkngyzqc",
        "description": "gsfoquwyzc",
        "name": "Christopher Patterson"
    },
    "parent_bundles": [
        {
            "seo_name": "siylshdjrl",
            "sku": "CC0F63F5F87A",
            "name": "ahfwaqayqe"
        }
    ],
    "product_line": {
        "code": "mjomjoqinu",
        "name": "hizgpokmoh"
    },
    "product_group": {
        "id": 6018591,
        "variation_products": [
            {
                "sku": "kfmfapbpjo",
                "attribute_values": [
                    {
                        "id": 1149332,
                        "code": "lsbmotzvws",
                        "values": [
                            "glywtpizcr",
                            "fenaawbtjc"
                        ]
                    },
                    {
                        "id": 3981478,
                        "code": "rmeoehjaht",
                        "values": [
                            "akezyjeukj",
                            "vhbidlmrhf"
                        ]
                    }
                ]
            }
        ],
        "variation_attributes": [
            {
                "id": 254,
                "code": "svpagsntrc",
                "name": "qmgfrpfeni"
            }
        ],
        "name": "Charles Jordan"
    },
    "bundle_products": [
        {
            "sku": "7E2AF12AD206",
            "name": "scqitpjcix",
            "seo_name": "tsptgekkrs",
            "quantity": 20,
            "priority": 575
        }
    ],
    "url": "xjmipvprec",
    "display_name": "bvvfxfnxwe",
    "seo_info": {
        "description": "voilertnkz",
        "meta_title": "nqvbduwlzv",
        "meta_description": "kzccqpqzju",
        "meta_keyword": "ethwhmjcqu",
        "short_description": "pnadhhtyiq"
    },
    "status": {
        "selling_status_code": "mejucgyihl",
        "publish_status": true
    },
    "attributes": [
        {
            "values": [
                {
                    "value": "vfsikhnauh",
                    "option_id": 6708524
                }
            ],
            "is_filterable": true,
            "is_comparable": false,
            "is_searchable": true,
            "code": "zbcjbvpidr",
            "name": "Daniel Ross",
            "id": 7020664,
            "priority": 1
        }
    ],
    "is_bundle": 1,
    "search_text": "donald schultz",
    "search_text_with_attribute": "donald schultz vfsikhnauh"
}"""

updated_at = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

insert_catalog_update_timestamp_valid = f"INSERT INTO product_details ( sku, data, catalog_status_code, created_at, updated_at) VALUES ('1254872016','{data}', null,'2019-05-24 09:17:31', '{updated_at}')"
del_catalog = "DELETE FROM product_details WHERE sku= '1254872016';"
promotions = """[{"channel": ["all"], "terminal": null, "definitions": [{"id": 22, "name": "TEST FOR ALL PRODUCT", "type": "product", "benefit": {"items": [], "money": [{"id": 36, "money": null, "percent": 20.0, "budget_id": 1, "max_discount": 200000.0, "budget_status": "active", "discount_type": "percent", "out_of_budget": false}]}, "channel": "all", "partner": "PHONGVU", "apply_on": "product", "ended_at": "2019-07-31T23:59:59+07:00", "condition": {"coupon": null, "order_value_max": null, "order_value_min": null, "payment_methods": ["all"]}, "is_default": true, "started_at": "2019-05-31T00:00:00+07:00", "description": "dasdas", "time_ranges": []}]}]
"""
promotion_prices = """[{"channel": ["all"], "terminal": null, "final_price": 11300000.0, "promotion_price": 11300000.0, "flash_sale_price": null}]"""
insert_ppm_update_timestamp_valid = f"INSERT INTO v_product_price_promotion ( sku, sell_price, supplier_sale_price, promotions, flash_sales, promotion_prices, updated_at) VALUES ('27091994', 11400000, 11400000,'{promotions}' , '[]', '{promotion_prices}','{updated_at}');"
del_ppm = "DELETE FROM v_product_price_promotion WHERE sku= '27091994';"
insert_promotion_count_update_timestamp_valid = f"INSERT INTO v_promotion_flash_sale_product ( sku, promo_past, promo_future, promo_current, fs_past, fs_future, fs_current, updated_at) VALUES ('1254872016', 5, 3, 2, 2, 11, 10, '{updated_at}');"
del_promotion_count = "DELETE FROM v_promotion_flash_sale_product WHERE sku= '1254872016';"
get_srm = """

select a.default_code as sku,
w.tk_price_include_tax as import_price, tax_out.tax_out, tax_in.tax_in,
c.tk_sale_point as sale_point
from product_product a
left join (select
 case when priceStartEnd.id is null
 then latest_price.tk_price_include_tax
 else priceStartEnd.tk_price_include_tax
 end,
 case when priceStartEnd.id is null
 then latest_price.product_id
 else priceStartEnd.product_id
 end
 from (select
 l.* from product_supplierinfo l
 join (select
 y.product_id, max(id) as max_id
 from product_supplierinfo y
 left join (select
 product_id, max(tk_price_include_tax) as max_price
 from product_supplierinfo
 where (date_start <= now() or date_start is null)
 and (date_end >= now() or date_end is null)
 group by product_id) h
 on y.product_id = h.product_id
 where y.tk_price_include_tax = h.max_price group by y.product_id) as s
 on l.id=s.max_id) priceStartEnd
 full outer join (select
 l.* from product_supplierinfo l
 join (select
 y.product_id,max (id) as max_id
 from product_supplierinfo y left join
 (select
 product_id, max(write_date) as lastest_write_date
 from product_supplierinfo m
 where write_date is not null
 group by m.product_id) z
 on y.product_id=z.product_id
 where y.write_date=z.lastest_write_date and y.product_id is not null group by y.product_id) k
 on l.id= k.max_id) latest_price
 on priceStartEnd.product_id=latest_price.product_id) w
on a.id = w.product_id
left join
 (select rel.prod_id , tax.amount as tax_in
 from product_supplier_taxes_rel rel
 JOIN account_tax tax ON rel.tax_id = tax.id
 ) tax_in
on tax_in.prod_id = a.product_tmpl_id
left join
 (select rel.prod_id , tax.amount as tax_out
 from product_taxes_rel rel
 JOIN account_tax tax ON rel.tax_id = tax.id
 ) tax_out
on tax_out.prod_id = a.product_tmpl_id
left join product_template c
on a.default_code = c.default_code
order by sku
"""
# time = datetime.datetime.utcnow()
# f"insert into shops ('created_at', 'updated_at', 'name', 'domain', 'activate', 'active_in_product_price' ) values ('{time}', '{time}', 'thunt_qc{i}', 'https://thunt_qc{i}.vn', random.choice(list), random.choice(list));"
