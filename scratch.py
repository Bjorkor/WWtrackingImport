import json
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# JSON data
jsonstring = '{"items":[{"base_currency_code":"USD","base_discount_amount":-2.78,"base_grand_total":64.62,"base_discount_tax_compensation_amount":0,"base_shipping_amount":7.65,"base_shipping_discount_tax_compensation_amnt":0,"base_shipping_incl_tax":8.18,"base_shipping_tax_amount":0.53,"base_subtotal":55.59,"base_subtotal_incl_tax":59.411,"base_tax_amount":4.16,"base_to_global_rate":1,"base_to_order_rate":1,"billing_address_id":617560,"created_at":"2023-04-05 15:43:58","discount_amount":-2.78,"discount_description":"5% off orders of $50+.","entity_id":292381,"global_currency_code":"USD","grand_total":64.62,"discount_tax_compensation_amount":0,"increment_id":"2000292381","order_currency_code":"USD","order_id":308780,"shipping_address_id":617559,"shipping_amount":7.65,"shipping_discount_tax_compensation_amount":0,"shipping_incl_tax":8.18,"shipping_tax_amount":0.53,"state":2,"store_currency_code":"USD","store_id":1,"store_to_base_rate":0,"store_to_order_rate":0,"subtotal":55.59,"subtotal_incl_tax":59.411,"tax_amount":4.16,"total_qty":1,"transaction_id":"44041767014","updated_at":"2023-04-05 15:43:59","items":[{"base_discount_amount":2.78,"base_discount_tax_compensation_amount":0,"base_price":55.59,"base_price_incl_tax":59.411,"base_row_total":55.59,"base_row_total_incl_tax":59.411,"base_tax_amount":3.63,"discount_amount":2.78,"entity_id":667069,"discount_tax_compensation_amount":0,"name":"Omega National Rubberwood Bread Board 3\\/4 x 18 x 23-1\\/2","parent_id":292381,"price":55.59,"price_incl_tax":59.411,"product_id":20146,"row_total":55.59,"row_total_incl_tax":59.411,"sku":"NPBB18","tax_amount":3.63,"order_item_id":706269,"qty":1}],"comments":[]}],"search_criteria":{"filter_groups":[{"filters":[{"field":"order_id","value":"308780","condition_type":"eq"}]}]},"total_count":1}'

# Load JSON data
data = json.loads(jsonstring)
order_data = data['items'][0]
order_item = order_data['items'][0]

# Create a PDF file
pdf = SimpleDocTemplate("order_invoice.pdf", pagesize=letter)
flowables = []

# Add invoice header
styles = getSampleStyleSheet()
header = Paragraph("Invoice", styles['Heading1'])
flowables.append(header)
flowables.append(Spacer(1, 20))

# Prepare the order details table
order_details_data = [
    ["Order ID", order_data['order_id']],
    ["Created at", order_data['created_at']],
    ["Updated at", order_data['updated_at']],
    ["Transaction ID", order_data['transaction_id']],
    ["Store ID", order_data['store_id']]
]
order_details_table = Table(order_details_data)
order_details_table.setStyle(TableStyle([
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 14),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT')
]))

flowables.append(order_details_table)
flowables.append(Spacer(1, 20))

# Prepare the item details table
item_details_data = [
    ["Item", "Price", "Qty", "Discount", "Tax", "Total"],
    [
        order_item['sku'],
        f"${order_item['price']:.2f}",
        order_item['qty'],
        f"${order_item['discount_amount']:.2f}",
        f"${order_item['tax_amount']:.2f}",
        f"${order_item['row_total']:.2f}"
    ]
]
item_details_table = Table(item_details_data)

# Apply item details table styles
item_details_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))

flowables.append(item_details_table)
flowables.append(Spacer(1, 20))

# Prepare the summary table
summary_data = [
    ["Subtotal", f"${order_data['subtotal']:.2f}"],
    ["Discount", f"${order_data['discount_amount']:.2f}"],
    ["Tax", f"${order_data['tax_amount']:.2f}"],
    ["Shipping", f"${order_data['shipping_amount']:.2f}"],
    ["Grand Total", f"${order_data['grand_total']:.2f}"]
]
summary_table = Table(summary_data)

# Apply summary table styles
summary_table.setStyle(TableStyle([
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 14),
    ('ALIGN', (0, 0), (-1, -1), 'RIGHT')
]))

flowables.append(summary_table)

# Build the PDF
pdf.build(flowables)
