import os
import base64
from PIL import Image, ImageDraw
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

def create_placeholder_assets():
    """Generates professional placeholders for logo.png, doctor.png, and kidney.png using PIL."""
    os.makedirs("assets", exist_ok=True)
    
    # 1. logo.png (Medical Shield Logo)
    logo_path = "assets/logo.png"
    if not os.path.exists(logo_path):
        img = Image.new("RGBA", (300, 300), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        # Draw a beautiful blue medical shield
        draw.polygon([(150, 20), (260, 60), (260, 200), (150, 280), (40, 200), (40, 60)], fill=(37, 99, 235, 255))
        # Draw inside shield
        draw.polygon([(150, 40), (240, 75), (240, 190), (150, 260), (60, 190), (60, 75)], fill=(30, 58, 138, 255))
        # Draw white cross
        draw.rectangle([135, 90, 165, 210], fill=(255, 255, 255, 255))
        draw.rectangle([90, 135, 210, 165], fill=(255, 255, 255, 255))
        img.save(logo_path, "PNG")
        
    # 2. doctor.png (Teal Doctor Avatar)
    doctor_path = "assets/doctor.png"
    if not os.path.exists(doctor_path):
        img = Image.new("RGBA", (300, 300), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        # Background Circle
        draw.ellipse([20, 20, 280, 280], fill=(16, 185, 129, 255))
        # Draw doctor shoulders/scrubs
        draw.chord([40, 160, 260, 340], 180, 360, fill=(30, 41, 59, 255))
        # Stethoscope (gray outline)
        draw.arc([90, 140, 210, 240], 0, 180, fill=(156, 163, 175, 255), width=10)
        # Draw face circle
        draw.ellipse([90, 50, 210, 170], fill=(253, 186, 116, 255))
        # Hair/Cap
        draw.chord([90, 50, 210, 120], 180, 360, fill=(13, 148, 136, 255))
        # Glasses/eyes
        draw.ellipse([110, 100, 140, 120], fill=(255, 255, 255, 255), outline=(51, 65, 85, 255), width=2)
        draw.ellipse([160, 100, 190, 120], fill=(255, 255, 255, 255), outline=(51, 65, 85, 255), width=2)
        draw.line([140, 110, 160, 110], fill=(51, 65, 85, 255), width=3)
        img.save(doctor_path, "PNG")
        
    # 3. kidney.png (Renal Organ Drawing)
    kidney_path = "assets/kidney.png"
    if not os.path.exists(kidney_path):
        img = Image.new("RGBA", (300, 300), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        # Left kidney bean shape
        draw.ellipse([50, 80, 140, 220], fill=(239, 68, 68, 255))
        # Inner crescent cutout
        draw.ellipse([85, 110, 145, 190], fill=(255, 255, 255, 0))
        # Right kidney bean shape
        draw.ellipse([160, 80, 250, 220], fill=(239, 68, 68, 255))
        # Inner crescent cutout
        draw.ellipse([155, 110, 215, 190], fill=(255, 255, 255, 0))
        # Ureters (lines)
        draw.line([125, 150, 150, 250], fill=(249, 115, 22, 255), width=8)
        draw.line([175, 150, 150, 250], fill=(249, 115, 22, 255), width=8)
        draw.line([150, 250, 150, 280], fill=(249, 115, 22, 255), width=8)
        img.save(kidney_path, "PNG")

def get_base64_image(image_path):
    """Encodes an image to base64 for embedding in inline styles."""
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

def inject_custom_css(dark_mode=False):
    """Injects high-fidelity custom CSS variables for animations, dark mode, cards, and warning alerts."""
    create_placeholder_assets()
    
    primary_color = "#2563EB"
    secondary_color = "#10B981"
    danger_color = "#EF4444"
    
    if dark_mode:
        bg_color = "#0F172A"
        card_bg = "rgba(30, 41, 59, 0.7)"
        card_border = "rgba(255, 255, 255, 0.1)"
        text_color = "#F8FAFC"
        text_muted = "#94A3B8"
        sidebar_bg = "#1E293B"
    else:
        bg_color = "#F8FAFC"
        card_bg = "rgba(255, 255, 255, 0.85)"
        card_border = "rgba(0, 0, 0, 0.05)"
        text_color = "#0F172A"
        text_muted = "#64748B"
        sidebar_bg = "#FFFFFF"

    css = f"""
    <style>
        /* Base page layout overrides */
        .stApp {{
            background: {bg_color};
            color: {text_color};
            font-family: 'Outfit', 'Inter', -apple-system, sans-serif;
            transition: all 0.3s ease;
        }}
        
        /* Glassmorphic Cards */
        .glass-card {{
            background: {card_bg};
            border: 1px solid {card_border};
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(12px);
            margin-bottom: 20px;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        
        .glass-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 15px 35px -5px rgba(37, 99, 235, 0.15);
        }}
        
        /* KPI Metrics custom styling */
        [data-testid="stMetricValue"] {{
            font-size: 2.2rem !important;
            font-weight: 700 !important;
            color: {primary_color} !important;
        }}
        
        /* Main Heading animations */
        .main-title {{
            font-weight: 800;
            background: linear-gradient(135deg, {primary_color}, {secondary_color});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.8rem;
            margin-bottom: 10px;
            animation: fadeIn 1s ease;
        }}
        
        /* Buttons custom styling */
        .stButton>button {{
            background: linear-gradient(135deg, {primary_color}, #1D4ED8) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 10px 24px !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25) !important;
            transition: all 0.2s ease !important;
        }}
        
        .stButton>button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4) !important;
        }}
        
        .stButton>button:active {{
            transform: translateY(1px) !important;
        }}
        
        /* Red Urgent Reset and Action Buttons */
        .danger-btn>button {{
            background: linear-gradient(135deg, {danger_color}, #DC2626) !important;
            box-shadow: 0 4px 12px rgba(239, 68, 68, 0.25) !important;
        }}
        
        .danger-btn>button:hover {{
            box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4) !important;
        }}
        
        /* High-risk Alerts */
        .blinking-alert {{
            background: rgba(239, 68, 68, 0.15);
            border: 2px solid {danger_color};
            color: {danger_color};
            border-radius: 12px;
            padding: 20px;
            margin-top: 15px;
            font-weight: bold;
            text-align: center;
            animation: pulse 1.5s infinite;
        }}
        
        @keyframes pulse {{
            0% {{ opacity: 0.7; transform: scale(0.99); }}
            50% {{ opacity: 1; transform: scale(1.01); }}
            100% {{ opacity: 0.7; transform: scale(0.99); }}
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        /* Subtitle */
        .sub-title {{
            color: {text_muted};
            font-size: 1.1rem;
            margin-bottom: 30px;
        }}
        
        /* Custom Sidebar style */
        [data-testid="stSidebar"] {{
            background-color: {sidebar_bg} !important;
            border-right: 1px solid {card_border} !important;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def generate_pdf_report(patient, prediction, ai_report, doctor_notes=""):
    """Compiles patient and prediction details into a clean PDF using ReportLab."""
    pdf_filename = f"reports/nephroguard_{patient['patient_id']}_{prediction['id']}.pdf"
    
    # Establish document setup
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=15,
        alignment=1 # Centered
    )
    
    header_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=colors.HexColor('#2563EB'),
        spaceBefore=12,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=6,
        leading=13
    )
    
    bold_body_style = ParagraphStyle(
        'BoldBody',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    
    warning_style = ParagraphStyle(
        'Warning',
        parent=body_style,
        textColor=colors.HexColor('#EF4444'),
        fontName='Helvetica-Bold'
    )

    story = []
    
    # Title
    story.append(Paragraph("NEPHROGUARD AI - CLINICAL REPORT", title_style))
    story.append(Paragraph("Intelligent Kidney Risk Assessment & Clinical Summary", ParagraphStyle('Sub', parent=body_style, alignment=1, fontSize=11, textColor=colors.HexColor('#64748B'))))
    story.append(Spacer(1, 15))
    
    # Metadata Table
    meta_data = [
        [Paragraph("<b>Patient Metadata</b>", bold_body_style), "", Paragraph("<b>Risk Summary</b>", bold_body_style), ""],
        [Paragraph("Patient ID:", body_style), Paragraph(patient['patient_id'], body_style), 
         Paragraph("Prediction Model:", body_style), Paragraph(prediction['model_name'], body_style)],
        [Paragraph("Full Name:", body_style), Paragraph(patient['name'], body_style), 
         Paragraph("Assessed Date:", body_style), Paragraph(prediction['prediction_date'][:16].replace('T', ' '), body_style)],
        [Paragraph("Age / Gender:", body_style), Paragraph(f"{patient['age']} yrs / {patient['gender']}", body_style), 
         Paragraph("Kidney Health Score:", body_style), Paragraph(f"<b>{prediction['kidney_health_score']:.0f}/100</b>", bold_body_style)],
        [Paragraph("Height / Weight:", body_style), Paragraph(f"{patient['height']} cm / {patient['weight']} kg", body_style), 
         Paragraph("Risk Classification:", body_style), Paragraph(f"<b>{prediction['risk_level']} ({prediction['probability'] * 100:.1f}%)</b>", bold_body_style)]
    ]
    
    meta_table = Table(meta_data, colWidths=[1.4*inch, 2.0*inch, 1.8*inch, 2.0*inch])
    meta_table.setStyle(TableStyle([
        ('SPAN', (0, 0), (1, 0)),
        ('SPAN', (2, 0), (3, 0)),
        ('BACKGROUND', (0, 0), (3, 0), colors.HexColor('#E2E8F0')),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 15))
    
    # Clinical Inputs Table
    story.append(Paragraph("Laboratory & Clinical Measurements", header_style))
    inputs = prediction['inputs']
    
    # Function to get yes/no for binary values
    def fmt_binary(val):
        return "Yes" if val == 1 else "No"
    
    inputs_data = [
        [Paragraph("Blood Pressure (mmHg):", body_style), Paragraph(str(inputs.get('blood_pressure', 'N/A')), body_style),
         Paragraph("Serum Creatinine (mg/dL):", body_style), Paragraph(str(inputs.get('serum_creatinine', 'N/A')), body_style)],
        [Paragraph("Blood Glucose (mg/dL):", body_style), Paragraph(str(inputs.get('blood_glucose', 'N/A')), body_style),
         Paragraph("Blood Urea (mg/dL):", body_style), Paragraph(str(inputs.get('blood_urea', 'N/A')), body_style)],
        [Paragraph("Albuminuria Grade:", body_style), Paragraph(f"Grade {inputs.get('albumin', 'N/A')}+", body_style),
         Paragraph("Hemoglobin (g/dL):", body_style), Paragraph(str(inputs.get('hemoglobin', 'N/A')), body_style)],
        [Paragraph("Sodium (mEq/L):", body_style), Paragraph(str(inputs.get('sodium', 'N/A')), body_style),
         Paragraph("Potassium (mEq/L):", body_style), Paragraph(str(inputs.get('potassium', 'N/A')), body_style)],
        [Paragraph("Hypertension Diagnosis:", body_style), Paragraph(fmt_binary(inputs.get('hypertension', 0)), body_style),
         Paragraph("Diabetes Diagnosis:", body_style), Paragraph(fmt_binary(inputs.get('diabetes', 0)), body_style)],
        [Paragraph("Smoking Status:", body_style), Paragraph(fmt_binary(inputs.get('smoking', 0)), body_style),
         Paragraph("Family History of Renal Failure:", body_style), Paragraph(fmt_binary(inputs.get('family_history', 0)), body_style)]
    ]
    
    inputs_table = Table(inputs_data, colWidths=[2.2*inch, 1.2*inch, 2.4*inch, 1.4*inch])
    inputs_table.setStyle(TableStyle([
        ('PADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ]))
    story.append(inputs_table)
    story.append(Spacer(1, 15))
    
    # Clinical AI Assessment
    story.append(Paragraph("AI-Generated Clinical Assessment", header_style))
    story.append(Paragraph(f"<b>Clinical Interpretation:</b> {ai_report['clinical_interpretation']}", body_style))
    story.append(Paragraph(f"<b>Key Risk Factors Identified:</b>", bold_body_style))
    for f in ai_report['risk_factors']:
        story.append(Paragraph(f"• {f}", body_style))
    story.append(Spacer(1, 8))
    
    # Recommendations Table
    story.append(Paragraph("Lifestyle and Dietary Recommendations", header_style))
    rec_data = [
        [Paragraph("<b>Category</b>", bold_body_style), Paragraph("<b>Clinical Recommendation</b>", bold_body_style)],
        [Paragraph("Diet Suggestions:", bold_body_style), Paragraph(ai_report['diet_suggestions'], body_style)],
        [Paragraph("Hydration Advice:", bold_body_style), Paragraph(ai_report['hydration_advice'], body_style)],
        [Paragraph("Exercise Regimen:", bold_body_style), Paragraph(ai_report['exercise_suggestions'], body_style)],
        [Paragraph("Medication Reminders:", bold_body_style), Paragraph(ai_report['medication_reminder'], body_style)],
        [Paragraph("Emergency Warning:", bold_body_style), Paragraph(ai_report['emergency_warning'], warning_style)]
    ]
    rec_table = Table(rec_data, colWidths=[1.8*inch, 5.4*inch])
    rec_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#F1F5F9')),
        ('PADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ]))
    story.append(rec_table)
    story.append(Spacer(1, 15))
    
    # Doctor Notes
    if doctor_notes:
        story.append(Paragraph("Attending Physician Notes & Observations", header_style))
        story.append(Paragraph(doctor_notes.replace("\n", "<br/>"), body_style))
        story.append(Spacer(1, 15))
        
    # Signature block
    sig_data = [
        ["", ""],
        [Paragraph("_____________________________<br/><b>Attending Clinician Signature</b>", body_style),
         Paragraph("_____________________________<br/><b>Authorized Hospital Seal</b>", body_style)]
    ]
    sig_table = Table(sig_data, colWidths=[3.6*inch, 3.6*inch])
    sig_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('PADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ]))
    story.append(sig_table)
    
    # Build Document
    doc.build(story)
    return pdf_filename
