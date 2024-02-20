from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import purple, green


c = canvas.Canvas("monthly_sales_report.pdf", pagesize=letter)
c.setTitle("Monthly Sales Report")

c.setFont("Helvetica", 12)
c.drawString(100, 750, "Monthly Sales Report - January 2024")
c.setFont("Helvetica", 10)
c.drawString(100, 735, "Overview:")
c.drawString(100, 720, "January saw a 10% increase in sales compared to December 2023.")
c.drawString(100, 705, "The growth was driven by the introduction of our new product line.")


data = [
    ["Region", "Product", "Units Sold", "Revenue"],
    ["North", "Widget A", 120, "$1,200"],
    ["South", "Widget B", 150, "$1,500"],
    ...
]

table = Table(data)
table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.grey),
    ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0,0), (-1,0), 12),
    ('GRID', (0,0), (-1,-1), 1, colors.black),
    ...
]))

table.wrapOn(c, width, height)
table.drawOn(c, *coord)



drawing = Drawing(400, 200)
data = [
    ((1, 1), (2, 2), (3, 3), (4, 5)),
    ((1, 2), (2, 3), (3, 4), (4, 6))
]
lp = LinePlot()
lp.x = 50
lp.y = 50
lp.height = 125
lp.width = 300
lp.data = data
lp.lines[0].strokeColor = purple
lp.lines[1].strokeColor = green

drawing.add(lp)
drawing.drawOn(c, 100, 500)


c.save()
