import io
import uuid
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from sqlalchemy.orm import Session
from app.repositories.report_repository import ReportRepository
from app.core.exceptions import ReportNotFoundException

class PDFService:
    """Service to generate a beautifully structured PDF summary of a medical report."""

    def __init__(self, db: Session) -> None:
        self._repo = ReportRepository(db)

    def generate_report_pdf(self, report_id: uuid.UUID, user_id: uuid.UUID) -> io.BytesIO:
        report = self._repo.get_by_id(report_id, user_id=user_id)
        if not report:
            raise ReportNotFoundException(str(report_id))

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        styles = getSampleStyleSheet()
        
        # Define custom styles
        primary_color = colors.HexColor("#1E40AF")  # Blue-800
        text_color = colors.HexColor("#1F2937")     # Gray-800
        border_color = colors.HexColor("#E5E7EB")   # Gray-200
        
        title_style = ParagraphStyle(
            'PDFTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=24,
            leading=28,
            textColor=primary_color,
            alignment=TA_LEFT,
            spaceAfter=15
        )
        
        subtitle_style = ParagraphStyle(
            'PDFSubtitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#4B5563"),  # Gray-600
            spaceAfter=20
        )

        section_heading = ParagraphStyle(
            'PDFSectionHeading',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=14,
            leading=18,
            textColor=primary_color,
            spaceBefore=15,
            spaceAfter=8,
            keepWithNext=True
        )

        body_style = ParagraphStyle(
            'PDFBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=text_color,
            spaceAfter=10
        )

        bullet_style = ParagraphStyle(
            'PDFBullet',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=text_color,
            leftIndent=15,
            firstLineIndent=-10,
            spaceAfter=5
        )

        disclaimer_style = ParagraphStyle(
            'PDFDisclaimer',
            parent=styles['Normal'],
            fontName='Helvetica-Oblique',
            fontSize=8,
            leading=11,
            textColor=colors.HexColor("#6B7280"),  # Gray-500
            spaceBefore=20
        )

        table_header_style = ParagraphStyle(
            'PDFTableHeader',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=9,
            leading=11,
            textColor=colors.white
        )

        table_cell_style = ParagraphStyle(
            'PDFTableCell',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=11,
            textColor=text_color
        )

        story = []

        # 1. Header
        story.append(Paragraph("HealthLens AI", title_style))
        report_date = report.created_at.strftime("%B %d, %Y at %I:%M %p")
        story.append(Paragraph(
            f"<b>Medical Report Summary</b><br/>"
            f"Report Name: {report.original_filename}<br/>"
            f"Date Processed: {report_date}",
            subtitle_style
        ))
        
        # Horizontal Rule
        story.append(Table(
            [['']], 
            colWidths=[532], 
            rowHeights=[1], 
            style=TableStyle([
                ('LINEABOVE', (0,0), (-1,-1), 1.5, primary_color),
                ('BOTTOMPADDING', (0,0), (-1,-1), 0),
                ('TOPPADDING', (0,0), (-1,-1), 0),
            ])
        ))
        story.append(Spacer(1, 15))

        # 2. AI Health Summary
        if getattr(report, "ai_summary", None):
            story.append(Paragraph("AI Health Summary", section_heading))
            summary_box_style = TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),  # Blue-50
                ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BFDBFE")),      # Blue-200
                ('TOPPADDING', (0,0), (-1,-1), 12),
                ('BOTTOMPADDING', (0,0), (-1,-1), 12),
                ('LEFTPADDING', (0,0), (-1,-1), 12),
                ('RIGHTPADDING', (0,0), (-1,-1), 12),
            ])
            summary_paragraph = Paragraph(report.ai_summary, ParagraphStyle(
                'PDFSummaryText',
                parent=body_style,
                textColor=colors.HexColor("#1E3A8A")  # Blue-900
            ))
            story.append(Table([[summary_paragraph]], colWidths=[532], style=summary_box_style))
            story.append(Spacer(1, 15))

        # 3. Markers Table
        markers = report.markers or []
        if markers:
            abnormal_markers = [m for m in markers if m.status and m.status.lower() in ("low", "high", "critical")]
            normal_markers = [m for m in markers if not m.status or m.status.lower() not in ("low", "high", "critical")]

            # Helper to create tables
            def build_marker_table(marker_list, header_bg):
                data = [[
                    Paragraph("Marker Name", table_header_style),
                    Paragraph("Value / Unit", table_header_style),
                    Paragraph("Reference Range", table_header_style),
                    Paragraph("Status", table_header_style)
                ]]
                for m in marker_list:
                    status_text = m.status or "Normal"
                    status_color = "#EF4444" if status_text.lower() in ("low", "high", "critical") else "#10B981"
                    
                    status_cell = Paragraph(
                        f"<font color='{status_color}'><b>{status_text.upper()}</b></font>",
                        table_cell_style
                    )
                    
                    data.append([
                        Paragraph(m.marker_name, table_cell_style),
                        Paragraph(f"{m.value or '—'} {m.unit or ''}", table_cell_style),
                        Paragraph(m.reference_range or "—", table_cell_style),
                        status_cell
                    ])

                t = Table(data, colWidths=[180, 120, 132, 100])
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), header_bg),
                    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                    ('TOPPADDING', (0,0), (-1,-1), 6),
                    ('GRID', (0,0), (-1,-1), 0.5, border_color),
                    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F9FAFB")]),
                ]))
                return t

            # Render Abnormal Markers
            if abnormal_markers:
                story.append(Paragraph("⚠️ Abnormal Markers", section_heading))
                story.append(build_marker_table(abnormal_markers, colors.HexColor("#EF4444")))
                story.append(Spacer(1, 15))

            # Render Normal Markers
            if normal_markers:
                story.append(Paragraph("Normal Markers", section_heading))
                story.append(build_marker_table(normal_markers, colors.HexColor("#10B981")))
                story.append(Spacer(1, 15))

        # 4. Doctor Consultation Prep Questions
        story.append(Paragraph("Questions to Ask Your Doctor", section_heading))
        story.append(Paragraph("Bring these questions to your next appointment to discuss with your healthcare provider:", body_style))
        
        # Dynamically reference abnormal markers in questions if present
        abnormal_names = [m.marker_name for m in markers if m.status and m.status.lower() in ("low", "high", "critical")]
        if abnormal_names:
            markers_str = ", ".join(abnormal_names[:3])
            story.append(Paragraph(f"• <b>About my abnormal values ({markers_str}):</b> What could be causing these specific markers to be out of range?", bullet_style))
            story.append(Paragraph("• <b>About lifestyle:</b> Are there specific dietary, exercise, or sleep changes I should make to address these markers?", bullet_style))
            story.append(Paragraph("• <b>About medication/supplements:</b> Do I need any medical treatments, prescriptions, or vitamin supplements?", bullet_style))
        else:
            story.append(Paragraph("• <b>General status:</b> Do my results indicate any early warning signs of chronic conditions?", bullet_style))
            story.append(Paragraph("• <b>Prevention:</b> What lifestyle changes can I adopt to maintain these healthy levels?", bullet_style))
            
        story.append(Paragraph("• <b>Follow-up:</b> When should I repeat these tests to track my trends?", bullet_style))
        story.append(Spacer(1, 10))

        # 5. Tips
        story.append(Paragraph("Tips for Your Appointment", section_heading))
        story.append(Paragraph("• Write down any symptoms you have been experiencing before you go.", bullet_style))
        story.append(Paragraph("• Keep a copy of this printed summary sheet to share directly with your provider.", bullet_style))
        story.append(Paragraph("• Bring a list of all current medications, vitamins, and supplements you take.", bullet_style))
        story.append(Spacer(1, 15))

        # 6. Disclaimer
        story.append(Paragraph(
            "<b>Disclaimer:</b> This report is generated by HealthLens AI for educational and informational purposes only. "
            "It does not constitute medical advice, diagnosis, or treatment. Always seek the advice of your physician or other "
            "qualified health provider with any questions you may have regarding a medical condition.",
            disclaimer_style
        ))

        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
