import os
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from django.conf import settings
from PIL import Image as PILImage
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def create_topic_pdf(topic):
    buffer = BytesIO()
    
    # Set up the document with larger margins for better readability
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(letter),
        rightMargin=1*inch,
        leftMargin=1*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    # Create styles with enhanced typography and spacing
    styles = getSampleStyleSheet()
    
    # Topic title style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=32,
        spaceAfter=40,
        spaceBefore=20,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#2C3E50'),
        leading=40  # Line height
    )
    
    # Topic description style
    description_style = ParagraphStyle(
        'TopicDescription',
        parent=styles['Normal'],
        fontSize=14,
        spaceAfter=30,
        spaceBefore=10,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor('#34495E'),
        leading=20,
        firstLineIndent=20
    )
    
    # Slide title style
    slide_title_style = ParagraphStyle(
        'SlideTitle',
        parent=styles['Heading2'],
        fontSize=24,
        spaceAfter=25,
        spaceBefore=35,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#2980B9'),
        leading=30,
        borderWidth=1,
        borderColor=colors.HexColor('#BDC3C7'),
        borderPadding=10,
        borderRadius=5
    )
    
    # Slide content style
    content_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=16,
        spaceAfter=20,
        spaceBefore=10,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor('#2C3E50'),
        leading=24,  # Increased line height for better readability
        firstLineIndent=20
    )

    # Story is the list of elements to build the PDF
    story = []

    # Add topic title with a colored background
    title_text = f'<font color="#2C3E50">{topic.title}</font>'
    story.append(Paragraph(title_text, title_style))
    
    # Add topic description if it exists
    if topic.description:
        story.append(Paragraph(topic.description, description_style))
    
    story.append(Spacer(1, 40))

    # Add slides
    for i, slide in enumerate(topic.slides.all().order_by('order')):
        # Add page break before each slide except the first one
        if i > 0:
            story.append(PageBreak())
        
        # Slide number
        slide_number = Paragraph(
            f'<font color="#95A5A6">Slide {i+1}</font>',
            ParagraphStyle(
                'SlideNumber',
                parent=styles['Normal'],
                fontSize=12,
                alignment=TA_RIGHT,
                textColor=colors.HexColor('#95A5A6')
            )
        )
        story.append(slide_number)
        story.append(Spacer(1, 20))
        
        # Slide title with styling
        title_text = f'<b>{slide.title}</b>'
        story.append(Paragraph(title_text, slide_title_style))
        
        # Slide content
        if slide.content:
            content_paragraphs = slide.content.split('\n')
            for paragraph in content_paragraphs:
                if paragraph.strip():  # Only add non-empty paragraphs
                    story.append(Paragraph(paragraph, content_style))
        
        # Handle image
        if slide.image:
            img_path = os.path.join(settings.MEDIA_ROOT, slide.image.name)
            if os.path.exists(img_path):
                img = PILImage.open(img_path)
                # Convert RGBA to RGB if necessary
                if img.mode in ('RGBA', 'LA'):
                    background = PILImage.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1])
                    img = background
                
                # Calculate image size to fit page while maintaining aspect ratio
                max_width = 7 * inch  # Slightly larger maximum width
                max_height = 4.5 * inch  # Slightly larger maximum height
                img_width, img_height = img.size
                aspect = img_width / float(img_height)
                
                if img_width > max_width:
                    img_width = max_width
                    img_height = img_width / aspect
                
                if img_height > max_height:
                    img_height = max_height
                    img_width = img_height * aspect
                
                # Center the image
                img = Image(img_path, width=img_width, height=img_height)
                img.hAlign = 'CENTER'  # Center align the image
                
                story.append(Spacer(1, 20))
                story.append(img)
        
        story.append(Spacer(1, 30))

    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer
